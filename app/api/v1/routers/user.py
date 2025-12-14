from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File

from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.user_schema import UserResponseSchema
from app.services.admin_service import get_current_admin
from app.services.user_service import get_current_user
from app.api.v1.crud import user_crud
from app.utils import enum_utils

from app.utils.log import ConsoleLogger as cl
from app.utils.storage_utils import upload_to_storage

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/user", tags=["User"])

@router.get("/get-user-info", response_model=UserResponseSchema)
async def get_user_info(user=Depends(get_current_user)):
    try:
        user_id = user.id
        result = user_crud.get_user_by_id(user_id)

        if not result.data:
            raise HTTPException(status_code=404, detail="User not found in public.users")

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update-user-info")
async def update_user_info(display_name: str = Form(None),
                           info: str = Form(None),
                           avatar: UploadFile = File(None),
                           user=Depends(get_current_user)):
    try:
        user_id = user.id
        avatar_url = None
        if avatar:
            file_path = f"avatars/{user_id}.jpg"
            avatar_url = await upload_to_storage(settings.IMAGE_BUCKET, file_path, avatar)
        update_data = {}

        if display_name is not None:
            update_data["user_display_name"] = display_name

        if info is not None:
            update_data["user_info"] = info

        if avatar_url:
            update_data["user_avatar_url"] = avatar_url

        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")

        res = user_crud.update_user_by_id(update_data, user_id)
        cl.info(res)

        if not res.data:
            raise HTTPException(status_code=400, detail="Update failed")

        res = user_crud.update_user_update_date_by_id(user_id)

        if not res.data:
            cl.warn("update user update date failed")

        return {"message": "Update successful"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-all-users")
def get_all_user(admin = Depends(get_current_admin)):
    try:
        admin_role = admin["admin_role"]
        if (not enum_utils.check_super_admin(admin_role) and
                not enum_utils.check_admin(admin_role) and
                not enum_utils.check_support_staff(admin_role)):
            raise HTTPException(status_code=403, detail="You don't have the authority to perform this action")

        result = user_crud.get_user()
        if not result.data:
            raise HTTPException(status_code=404, detail="Users not found")

        return result.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get all users error: {e}")