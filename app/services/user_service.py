import requests
from fastapi import Header, HTTPException

from app.core.config import Settings

settings = Settings()

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
        "apikey": settings.SUPABASE_KEY
    }
    try:
        user_response = requests.get(f"{settings.SUPABASE_URL}/auth/v1/user", headers=headers)

        if user_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = user_response.json()

        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
