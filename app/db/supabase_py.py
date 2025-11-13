from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_py:Client = create_client(SUPABASE_URL, SUPABASE_KEY)



# data = supabase.table('Users').select('*').execute()
# print(data)
