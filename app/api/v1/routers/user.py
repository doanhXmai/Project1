from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File

from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.user_schema import UserResponseSchema
from app.services.user_service import get_current_user
from app.api.v1.crud import user_crud

from app.utils.log import ConsoleLogger as cl
from app.utils.storage_utils import upload_to_storage

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/user", tags=["User"])

@router.get("/get-user-info", response_model=UserResponseSchema)
async def get_user_info(user=Depends(get_current_user)):
    try:
        user_id = user["id"]
        result = user_crud.get_user_by_id(user_id)

        if not result.data:
            raise HTTPException(status_code=404, detail="User not found in public.users")

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update-user-info")
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
        update_data = {
            "user_display_name": display_name,
            "user_info": info
        }

        if avatar_url:
            update_data["user_avatar_url"] = avatar_url

        res = user_crud.update_user_by_id(update_data, user_id)
        cl.info(res)

        return {"message": "Update successful", "avatar_url": avatar_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))