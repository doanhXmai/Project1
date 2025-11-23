from fastapi import APIRouter, HTTPException

from app.core.config import Settings
from app.core.supabase import supabase_py

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/Singer", tags=["Singer"])

@router.get("/get-all-singers")
def get_all_singers():
    try:
        result = supabase_py.table("Singers").select("*").execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found in Singers")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))