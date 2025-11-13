from fastapi import APIRouter, Header, HTTPException, Depends
import requests

import os
from dotenv import load_dotenv

from app.db.supabase_py import supabase_py, SUPABASE_KEY, SUPABASE_URL

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/api/v1/user", tags=["User"])

async def get_current_user(authorization: str = Header(...)):
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
            # "auth_user":{
            #     "id": user["id"],
            #     "email": user["email"]
            #     # "create_at": user["created at"]
            # },
            "public_user": {
                "email": user_record.get("user_email"),
                "phone": user_record.get("user_phone"),
                "name": user_record.get("user_name"),
                "role": user_record.get("user_role"),
                "info": user_record.get("user_info"),
                "create_date": user_record.get("user_create_date"),
                "avatar": user_record.get("user_avatar_url")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))