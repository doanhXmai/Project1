from uuid import UUID

from pydantic import EmailStr

from app.utils.log import ConsoleLogger as cl
from app.core.supabase import supabase_py

def check_user_field(field, query) -> bool:
    try:
        if query not in ["user_id", "user_name", "user_email", "user_phone"]:
            raise ValueError("Invalid field")
        result = supabase_py.table("Users").select("*").eq(query, field).excute()

        return bool(result.data)

    except Exception as e:
        cl.error(f"Check {query} of user error: {e}")
        return False

def check_user(user_id: UUID = None, user_name: EmailStr = None, user_email: str = None, user_phone: str = None):
    allowed_fields = {
        "id": "user_id",
        "name": "user_name",
        "email": "user_email",
        "phone": "user_phone"
    }
    if user_id: return check_user_field(user_id, allowed_fields["id"])
    if user_name: return check_user_field(user_name, allowed_fields["name"])
    if user_email: return check_user_field(user_email, allowed_fields["email"])
    if user_phone: return check_user_field(user_phone, allowed_fields["phone"])
    return False