from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.password_resets_schema import PasswordResetsCreateSchema

settings = Settings()

def create_password_resets(password_resets: PasswordResetsCreateSchema):
    return supabase_py_service_client.table("PasswordResets").insert({
        "passwordResets_user_id": str(password_resets.passwordResets_user_id),
        "passwordResets_email": password_resets.passwordResets_email,
        "passwordResets_otp_code": password_resets.passwordResets_otp_code,
        "passwordResets_expired_at": password_resets.passwordResets_expired_at if isinstance(password_resets.passwordResets_expired_at, str) else password_resets.passwordResets_expired_at.isoformat(),
        "passwordResets_created_at": settings.DATE_NOW.isoformat(),
        "passwordResets_used": False
    }).execute()

def get_valid_otp(email: str, otp: str):
    return (supabase_py_service_client.table("PasswordResets")
            .select("*")
            .eq("passwordResets_email", email)
            .eq("passwordResets_otp_code", otp)
            .eq("passwordResets_used", False)
            .execute())

def mark_otp_used(record_id: str):
    return (supabase_py_service_client.table("PasswordResets")
            .update({"passwordResets_used": True})
            .eq("passwordResets_id", record_id)
            .execute())