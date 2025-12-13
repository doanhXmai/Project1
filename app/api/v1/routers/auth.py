from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.crud.auth_crud import update_user_password_by_id
from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.auth_schema import RegisterRequestByEmail, VerifyOtp
from app.schemas.auth_schema import LoginRequestByEmail
from app.schemas.auth_schema import RefreshTokenRequest
from app.schemas.auth_schema import ForgotPasswordRequestByEmail
from app.schemas.auth_schema import ChangePasswordRequestByEmail
from app.api.v1.crud import user_crud, password_resets_crud, auth_crud
from app.schemas.password_resets_schema import PasswordResetsCreateSchema
from app.services.user_service import get_current_user
from app.utils.email_utils import send_otp_email
from app.utils.generate_otp import generate_otp

from app.utils.log import ConsoleLogger as cl

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/auth", tags=["Auth"])

# use email
@router.post("/register-by-email")
def register_user_by_email(request: RegisterRequestByEmail):
    try:
        check_admin = supabase_py_service_client.table("Admins").select("*").eq("admin_email", request.email).execute()
        if check_admin.data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        response = supabase_py_service_client.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        if response.user is None:
            raise HTTPException(status_code=400, detail=response)
        return {"message": "Register successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Register account error: {e}")

@router.post("/login-by-email")
def login_user_by_email(request: LoginRequestByEmail):
    try:
        response = supabase_py_service_client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email or password incorrect")


    user_id = response.user.id

    user_record = user_crud.get_user_by_id(user_id)

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
        response = auth_crud.refresh_access_token(request.refresh_token)

        if response is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/request-password-reset")
def request_password_reset(req: ForgotPasswordRequestByEmail):
    try:
        email = req.email.lower()

        user = user_crud.get_user_by_email(email)
        if not user.data:
            raise HTTPException(status_code=404, detail="Email not found")

        otp = generate_otp(100000, 999999)

        password_resets_crud.create_password_resets(PasswordResetsCreateSchema(
            passwordResets_user_id=user.data[0]["user_id"],
            passwordResets_email=email,
            passwordResets_otp_code=otp,
            passwordResets_expired_at=(datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        ))

        send = send_otp_email(to_email=email, otp_code=otp)

        return {"status": send, "message": "OTP send successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request password reset error: {e}")

@router.post("/verify-otp-reset-password")
def verify_otp_reset_password(request: VerifyOtp):
    try:
        res = password_resets_crud.get_valid_otp(email=request.email, otp=request.otp)

        cl.info(f"email: {request.email}")
        cl.info(f"OTP: {request.otp}")

        if not res.data:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        record = res.data[0]

        expires_at = datetime.fromisoformat(
            record["passwordResets_expired_at"].replace('Z', "+00:00")
        )

        now = settings.DATE_NOW

        if now > expires_at:
            raise HTTPException(status_code=400, detail="OTP expired")

        mark_otp = password_resets_crud.mark_otp_used(record["passwordResets_id"])

        used = mark_otp.data[0]["passwordResets_used"]
        user_id = record["passwordResets_user_id"]
        try:
            auth_update = update_user_password_by_id(user_id, request.new_password)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update password in Auth system - {e}")

        return {
            "message": "OTP verified successfully",
            "email": request.email,
            "success": used
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/change-password-by-email")
def change_password_by_email(request: ChangePasswordRequestByEmail, user=Depends(get_current_user)):
    try:
        user_id = user.id

        login_resp = supabase_py_service_client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.old_password
        })
        if not login_resp.user:
            raise HTTPException(status_code=401, detail="Old password is incorrect")
        access_token = login_resp.session.access_token
        supabase_py_service_client.auth.update_user(
            { "password": request.new_password },
            { "access_token": access_token }
        )
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))