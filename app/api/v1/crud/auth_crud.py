from uuid import UUID

from app.core.supabase import supabase_py_service_client


def update_user_password_by_id(user_id: UUID, password: str):
    return supabase_py_service_client.auth.admin.update_user_by_id(
        uid=user_id,
        attributes={"password": password}
    )

def refresh_access_token(refresh_token):
    return supabase_py_service_client.auth.refresh_session(refresh_token)