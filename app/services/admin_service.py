from datetime import datetime, timezone

from fastapi import HTTPException, Header

from uuid import UUID

from pydantic import EmailStr

from app.enums.enums import AdminRoleEnum
from app.schemas.admin_schema import AdminResponseSchema, AdminCreateSchema
from app.utils.auth_utils import verify_access_token
from app.utils.enum_utils import change_role_enum
from app.api.v1.crud import admin_crud, user_crud

# ============== get admin from token =================#
async def  get_current_admin(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    admin_id = verify_access_token(token)
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    result = admin_crud.get_admin_by_id(admin_id)
    if not result.data or not result.data[0]["admin_status"]:
        raise HTTPException(status_code=403, detail="Admin not found or inactive")

    return result.data[0]

def admin_login(admin_name: str, admin_email: EmailStr, admin_phone: str):
    try:
        return admin_crud.get_admin(admin_name, admin_email, admin_phone)
    except Exception as e:
        print ("admin login in  crud error: ", e)
        return None

# ============== check admin exist =================#
async def check_admin(account_info: AdminCreateSchema):
    check_name = admin_crud.get_admin_by_name(account_info.admin_name)
    check_email = admin_crud.get_admin_by_email(account_info.admin_email)
    check_phone = admin_crud.get_admin_by_phone(account_info.admin_phone)

    if check_name.data or check_email.data or check_phone.data:
        return True
    return False

# ============== create account admin =================#
async def create_account(account_info: AdminCreateSchema):
    if await check_admin(account_info):
        return False, "Admin already exits"
    try:
        admin_crud.create_admin(account_info)
        return True, "Create admin successfully"
    except Exception as e:
        print("Create account error: ", e)
        return False, f"Error when creating admin: {e}"

# ============== check role =================#
def can_create(target_role: AdminRoleEnum, create_role: AdminRoleEnum):
    if create_role < AdminRoleEnum.ADMIN:
        return False
    return create_role.level > target_role.level

# ============== create admin =================#
async def create_admin(admin_creator: AdminResponseSchema, account_info: AdminCreateSchema):
    try:
        creator_role = change_role_enum(admin_creator["admin_role"])
        target_role = change_role_enum(account_info.admin_role)
    except ValueError:
        return False, "Invalid role format"

    if not can_create(target_role, creator_role):
        return False, "You don't have permission to create this role"

    status, msg = await create_account(account_info = account_info)
    return status, msg

# ============== checking role to disable or enable =================#
def can_disable_or_enable_user(role: AdminRoleEnum):
    if role == AdminRoleEnum.MODERATOR or role == AdminRoleEnum.CONTENT_MANAGER:
        return False, "You don't have permission to disable account"

    return True, "You have permission to disable account"

def can_disable_or_enable_admin(role: AdminRoleEnum, target_role: AdminRoleEnum):
    if role == target_role:
        return False, "You don't have permission to disable admin"
    if role >= AdminRoleEnum.ADMIN:
        return True, "You have permission to disable admin"

    return False, "You don't have permission to disable admin"

# ============== disable or enable account ================= #
def disable_or_enable_user(role: AdminRoleEnum, user_id: UUID, switch: bool = False):
    try:
        check, msg = can_disable_or_enable_user(role = role)
        if not check:
            return check, msg

        result = user_crud.update_user_status_by_id(user_id, switch)

        if len(result.data) == 0:
            return False, "User not found"

        return True, f"You disabled or enabled the user with ID: {user_id} successfully"
    except Exception as e:
        return False, f"You are getting error: {e}"

def disable_or_enable_admin(role: AdminRoleEnum, admin_id: int, switch: bool = False):
    try:
        target_role = admin_crud.get_admin_role_by_id(admin_id)

        check, msg = can_disable_or_enable_admin(role = role, target_role = change_role_enum(target_role))
        if not check: return check, msg

        result = admin_crud.update_admin_status_by_id(admin_id, switch)

        if len(result.data) == 0:
            return False, "Admin not found"

        return True, f"You disabled or enabled the admin with ID: {admin_id} successfully"
    except Exception as e:
        return False, f"You are getting error: {e}"
