from fastapi import APIRouter, HTTPException, Depends

from uuid import UUID


from app.api.v1.crud.admin_crud import admin_login
from app.core.config import Settings
from app.schemas.admin_schema import LoginRequest, AdminResponseSchema, TokenResponse, AdminCreateSchema, \
    DisableAdminRequest
from app.schemas.default_schema import DefaultSuccessful
from app.schemas.user_schema import DisableUserRequest
from app.services.admin_service import get_current_admin, create_admin, disable_or_enable_user, disable_or_enable_admin
from app.utils.auth_utils import create_access_token
from app.utils.enum_utils import change_role_enum
from app.utils.password_utils import verify_password

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/admin", tags=["Admin"])

# ============== login =================#
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    try:
        result = admin_login(admin_name=request.name, admin_email=request.email, admin_phone=request.phone)

        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid email or phone or name")

        admin = result.data[0]

        if not admin["admin_status"]:
            raise HTTPException(status_code=403, detail="Admin account is inactive")

        if verify_password(request.password, admin["admin_password"]) is False:
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token(admin["admin_id"])
        return {"access_token": token, "token_type": "bearer", "role": result.data[0]["admin_role"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== get - info =================#
@router.get("/info", response_model=AdminResponseSchema)
def get_admin_info(admin=Depends(get_current_admin)):
    return admin

# ============== get - info =================#
@router.post("/create-admin", response_model=DefaultSuccessful)
async def create_account_admin(account_info: AdminCreateSchema, admin=Depends(get_current_admin)):
    try:
        status, msg = await create_admin(
            admin_creator=admin,
            account_info=account_info
        )

        if not status:
            # Không đủ quyền
            if msg == "You don't have permission to create this role":
                raise HTTPException(status_code=403, detail=msg)

            # Lỗi logic khác
            raise HTTPException(status_code=400, detail=msg)

        return DefaultSuccessful(
            message = msg,
            success = status
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== disable account =================#
@router.post("/disable-user", response_model=DefaultSuccessful)
def disable_account_user(data: DisableUserRequest, admin=Depends(get_current_admin)):
    status, msg = disable_or_enable_user(change_role_enum(admin["admin_role"]), data.user_id)
    return DefaultSuccessful(
        message = msg,
        success = status
    )

@router.post("/disable-admin", response_model=DefaultSuccessful)
def disable_account_admin(data: DisableAdminRequest, admin=Depends(get_current_admin)):
    if data.admin_id == admin["admin_id"]:
        raise HTTPException(status_code=500, detail="You cannot disable your own admin account")

    status, msg = disable_or_enable_admin(change_role_enum(admin["admin_role"]), data.admin_id)
    return DefaultSuccessful(
        message = msg,
        success = status
    )

# ============== enable account =================#
@router.post("/enable-user", response_model=DefaultSuccessful)
def enable_account_user(data: DisableUserRequest, admin=Depends(get_current_admin)):
    status, msg = disable_or_enable_user(change_role_enum(admin["admin_role"]), data.user_id, switch=True)
    return DefaultSuccessful(
        message = msg,
        success = status
    )

@router.post("/enable-admin", response_model=DefaultSuccessful)
def enable_account_admin(data: DisableAdminRequest, admin=Depends(get_current_admin)):
    if data.admin_id == admin["admin_id"]:
        raise HTTPException(status_code=500, detail="You cannot disable your own admin account")

    status, msg = disable_or_enable_admin(change_role_enum(admin["admin_role"]), data.admin_id, switch=True)
    return DefaultSuccessful(
        message = msg,
        success = status
    )