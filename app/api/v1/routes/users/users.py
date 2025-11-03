from fastapi import APIRouter, Request, HTTPException, Depends
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

from app.db.supabase_py import supabase_py

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/user", tags=["User"])

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm = [ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")


@router.get("/me")
def get_user_info(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    user = supabase_py.table("Users").select("*").eq("user_id", user_id).execute()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "status": "success",
        "data": {
            "id": user.user_id,
            "name": user.user_display_name,
            "email": user.email
        }
    }