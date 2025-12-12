from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.genre_schema import GenreCreateSchema


def get_all():
    return supabase_py_service_client.table("Genres").select("*").execute()

def get_genre_id_by_name(name: str):
    return supabase_py_service_client.table("Genres").select("genre_id").eq("genre_name", name).execute()

def get_genre_by_name(name: str):
    return supabase_py_service_client.table("Genres").select("*").eq("genre_name", name).execute()

def get_genre_by_id(genre_id: int):
    return supabase_py.table("Genres").select("*").eq("genre_id", genre_id).execute()

def create_genre(genre: GenreCreateSchema):
    return supabase_py_service_client.table("Genres").insert({
        "genre_name": genre.genre_name,
        "genre_info": genre.genre_info
    }).execute()

def update_genre(genre_id, genre: GenreCreateSchema):
    return supabase_py_service_client.table("Genres").update({
                 "genre_name": genre.genre_name,
                 "genre_info": genre.genre_info
             }).eq("genre_id", genre_id).execute()