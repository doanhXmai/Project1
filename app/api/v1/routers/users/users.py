from fastapi import APIRouter, Header, HTTPException, Depends, Form, UploadFile, File
import requests

import os
from dotenv import load_dotenv

from app.db.supabase_py import supabase_py, SUPABASE_KEY, SUPABASE_URL, supabase_py_service_client

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/api/v1/user", tags=["User"])

async def get_current_user(authorization: str = Header(...)):
    """
    Lấy access token từ header của request
    :param authorization:
    :return: user
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    access_token = authorization.split(" ")[1]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "apikey": SUPABASE_KEY
    }
    try:
        user_response = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = user_response.json()

        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")

@router.get("/get-user-info")
async def get_user_info(user=Depends(get_current_user)):
    try:
        user_id = user["id"]
        result = supabase_py.table("Users").select("*").eq("user_id", user_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="User not found in public.users")
        user_record = result.data[0]
        return {
            "public_user": {
                "email": user_record.get("user_email"),
                "phone": user_record.get("user_phone"),
                "name": user_record.get("user_display_name"),
                "role": user_record.get("user_role"),
                "info": user_record.get("user_info"),
                "create_date": user_record.get("user_create_date"),
                "avatar": user_record.get("user_avatar_url")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update-user-info")
async def update_user_info(display_name: str = Form(None),
                           info: str = Form(None),
                           avatar: UploadFile = File(None),
                           user=Depends(get_current_user)):
    try:
        user_id = user["id"]
        print(user_id)
        avatar_url = None
        if avatar:
            file_bytes = await avatar.read()
            file_path = f"avatars/{user_id}.jpg"
            try:
                supabase_py_service_client.storage.from_("images").remove([file_path])
            except Exception as e:
                print("Không có file xoá")
                pass
            supabase_py_service_client.storage.from_("images").upload(
                file_path, file_bytes, {"content-type": avatar.content_type}
            )
            avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/images/{file_path}"
        print(avatar_url)
        update_data = {
            "user_display_name": display_name,
            "user_info": info
        }

        if avatar_url:
            update_data["user_avatar_url"] = avatar_url

        res = supabase_py_service_client.table("Users").update(update_data).eq("user_id", user_id).execute()
        print(res)
        return {"message": "Update successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))