from fastapi import APIRouter , HTTPException, status

from app.core.config import Settings
from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.auth_schema import RegisterRequestByEmail
from app.schemas.auth_schema import LoginRequestByEmail
from app.schemas.auth_schema import RefreshTokenRequest
from app.schemas.auth_schema import ForgotPasswordRequestByEmail
from app.schemas.auth_schema import ResetPasswordRequest
from app.schemas.auth_schema import ChangePasswordRequestByEmail

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/auth", tags=["Auth"])

# use email
@router.post("/register-by-email")
def register_user_by_email(request: RegisterRequestByEmail):
    check_admin = supabase_py_service_client.table("Admins").select("*").eq("admin_email", request.email).execute()
    if check_admin.data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "Email already exists")

    response = supabase_py.auth.sign_up({
        "email": request.email,
        "password": request.password
    })
    if response.user is None:
        raise HTTPException(status_code=400, detail = response)
    return {"message": "Register successful"}

@router.post("/login-by-email")
def login_user_by_email(request: LoginRequestByEmail):
    response = supabase_py.auth.sign_in_with_password({
        "email": request.email,
        "password": request.password
    })

    user_id = response.user.id

    user_record = supabase_py.table("Users").select("*").eq("user_id", user_id).execute()

    if not user_record.data:
        raise HTTPException(status_code=404, detail="User not in public.Users")

    if user_record.data[0]["user_status"] is False:
        raise HTTPException(status_code=403, detail="Account is disabled")

    if response.session is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }

@router.post("/refresh-access-token")
def refresh_access_token(request: RefreshTokenRequest):
    try:
        response = supabase_py.auth.refresh_session(request.refresh_token)

        if response is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/forgot-password-by-email")
def forgot_password_by_email(request: ForgotPasswordRequestByEmail):
    try:
        supabase_py.auth.reset_password_email(request.email)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    try:
        supabase_py.auth.update_user(
            {
                "password": request.new_password
            },
            {
                "access_token": request.access_token
            }
        )
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-password-by-email")
def change_password_by_email(request: ChangePasswordRequestByEmail):
    try:
        login_resp = supabase_py.auth.sign_in_with_password({
            "email": request.email,
            "password": request.old_password
        })
        if not login_resp.user:
            raise HTTPException(status_code=401, detail="Old password is incorrect")
        access_token = login_resp.session.access_token
        supabase_py.auth.update_user(
            { "password": request.new_password },
            { "access_token": access_token}
        )
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))