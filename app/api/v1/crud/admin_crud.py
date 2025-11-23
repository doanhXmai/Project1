from pydantic import EmailStr

from app.core.supabase import supabase_py


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
