from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.singer_schema import SingerCreateSchema


def get_all():
    return supabase_py_service_client.table("Singers").select("*").execute()

def get_singer_id_by_name(name: str):
    return supabase_py_service_client.table("Singers").select("singer_id").eq("singer_name", name).execute()

def get_singer_by_id(singer_id: int):
    return supabase_py.table("Singers").select("*").eq("singer_id", singer_id).execute()

def get_singer_by_name(singer_name: str):
    return supabase_py.table("Singers").select("*").eq("singer_name", singer_name).execute()

def create_singer(singer: SingerCreateSchema):
    return supabase_py_service_client.table("Singers").insert({
        "singer_name": singer.singer_name,
        "singer_info": singer.singer_info,
        "singer_view": 0
    }).execute()

def update_singer(singer_id, singer: SingerCreateSchema):
    return supabase_py_service_client.table("Singers").update({
        "singer_name": singer.singer_name,
        "singer_info": singer.singer_info,
        "singer_view": singer.singer_view
    }).eq("singer_id", singer_id).execute()