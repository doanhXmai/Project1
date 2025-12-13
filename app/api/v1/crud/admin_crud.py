from pydantic import EmailStr

from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.admin_schema import AdminCreateSchema
from app.utils.log import ConsoleLogger as cl
from app.utils.password_utils import hash_password

settings = Settings()

def get_admin(admin_name: str, admin_email: EmailStr, admin_phone: str):
    return (supabase_py_service_client
            .table("Admins")
            .select("*")
            .eq("admin_name", admin_name)
            .eq("admin_email", admin_email)
            .eq("admin_phone", admin_phone)
            .execute())

def get_all_admins():
    return supabase_py_service_client.table("Admins").select("admin_id, admin_name, admin_email, admin_phone, admin_status, admin_role").execute()

def get_admin_by_id(admin_id: int):
    return supabase_py_service_client.table("Admins").select("*").eq("admin_id", admin_id).execute()

def get_admin_role_by_id(admin_id: int):
    return supabase_py_service_client.table("Admins").select("admin_role").eq("admin_id", admin_id).execute()

def get_admin_by_email(admin_email: EmailStr):
    return supabase_py_service_client.table("Admins").select("*").eq("admin_email", admin_email).execute()

def get_admin_by_name(admin_name: str):
    return supabase_py_service_client.table("Admins").select("*").eq("admin_name", admin_name).execute()

def get_admin_by_phone(admin_phone: str):
    return supabase_py_service_client.table("Admins").select("*").eq("admin_phone", admin_phone).execute()

def create_admin(admin_in: AdminCreateSchema):
    supabase_py_service_client.table("Admins").insert({
        "admin_email": admin_in.admin_email,
        "admin_phone": admin_in.admin_phone,
        "admin_name": admin_in.admin_name,
        "admin_password": hash_password(admin_in.admin_password),
        "admin_role": admin_in.admin_role,
        "admin_display_name": admin_in.admin_display_name,
        "admin_create_date": settings.DATE_NOW.isoformat(),
        "admin_status": True
    }).execute()

def update_admin_status_by_id(admin_id: int, status: bool = False):
    return supabase_py_service_client.table("Admins").update({"admin_status": status}).eq("admin_id", admin_id).execute()


def check_admin_field(field, query) -> bool:
    try:
        if query not in ["admin_id", "admin_name", "admin_email", "admin_phone"]:
            raise ValueError("Invalid field")

        result = supabase_py_service_client.table("Admins").select("*").eq(query, field).execute()
        return bool(result.data)

    except Exception as e:
        cl.error(f"Check {query} of admin error: {e}")
        return False

def check_admin(admin_id: int = None, admin_name: str = None, admin_email: EmailStr = None, admin_phone: str = None):
    allowed_fields = {
        "id": "admin_id",
        "name": "admin_name",
        "email": "admin_email",
        "phone": "admin_phone"
    }
    if admin_id: return check_admin_field(admin_id, allowed_fields["id"])
    if admin_name: return check_admin_field(admin_name, allowed_fields["name"])
    if admin_email: return check_admin_field(admin_email, allowed_fields["email"])
    if admin_phone: return check_admin_field(admin_phone, allowed_fields["phone"])
    return False