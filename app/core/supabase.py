from supabase import create_client, Client

from app.core.config import get_settings

settings = get_settings()

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
SUPABASE_SERVICE_ROLE = settings.SUPABASE_SERVICE_ROLE

supabase_py:Client = create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_py_service_client = create_client(SUPABASE_URL, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvbHpjc2psaGd0ZHhiaWh4ZWJsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTg1NTYyNiwiZXhwIjoyMDc1NDMxNjI2fQ.tfbCPIErc3szR7Ibd9mCA-gwGClp3uPIMdwVOxeBIDQ")
