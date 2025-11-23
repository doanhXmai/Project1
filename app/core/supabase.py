from supabase import create_client, Client

from app.core.config import get_settings

settings = get_settings()

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
SUPABASE_SERVICE_ROLE = settings.SUPABASE_SERVICE_ROLE

supabase_py:Client = create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_py_service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

