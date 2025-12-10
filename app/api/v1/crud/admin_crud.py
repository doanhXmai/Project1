from pydantic import EmailStr

from app.core.supabase import supabase_py
from app.utils.log import ConsoleLogger as cl

def admin_login(admin_name: str, admin_email: EmailStr, admin_phone: str):
    try:
        return (supabase_py
                                    .table("Admins")
                                    .select("*")
                                    .eq("admin_name", admin_name)
                                    .eq("admin_email", admin_email)
                                    .eq("admin_phone", admin_phone)
                                    .execute())
    except Exception as e:
        print ("admin login in  crud error: ", e)
        return None

def check_admin_field(field, query) -> bool:
    try:
        if query not in ["admin_id", "admin_name", "admin_email", "admin_phone"]:
            raise ValueError("Invalid field")
        result = supabase_py.table("Admins").select("*").eq(query, field).excute()
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