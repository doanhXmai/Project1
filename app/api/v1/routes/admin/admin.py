from fastapi import APIRouter, HTTPException

from app.db.supabase_py import supabase_py
from .admin_helper import LoginRequest

router = APIRouter(prefix="/admin", tags=["Admin"])

# ============== login =================#
# use email
@router.post("/login")
def login(request: LoginRequest):
    try:
        column_map = {
            "email": "admin_email",
            "phone": "admin_phone",
            "name": "admin_name"
        }
        if LoginRequest.login_type not in column_map:
            raise HTTPException(status_code=400, detail="Invalid login type")

        result = ((supabase_py.table("Admins").select("*")
                   .eq(column_map[request.login_type], request.value)
                   .eq("admin_password", request.password))
                  .execute())
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {"status": "success", "message": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))