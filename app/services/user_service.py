from fastapi import Header, HTTPException

from app.core.supabase import supabase_py

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth format")

    access_token = authorization.split(" ")[1]

    try:
        user = supabase_py.auth.get_user(access_token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return user.user  # trả về thông tin user
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalid or expired")
