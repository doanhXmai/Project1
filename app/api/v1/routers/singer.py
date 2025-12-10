from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.core.config import Settings
from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.singer_schema import SingerCreateSchema
from app.services.user_service import get_current_user

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

# @router.post("/add-singer-user")
# def add_singer(request: SingerCreateSchema, user=Depends(get_current_user)):
    # try:
