from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.genre_schema import GenreCreateSchema, GenreResponseSchema


def get_or_create_genre(genre_in: GenreCreateSchema):
    try:
        result = supabase_py.table("Genres").select("*").eq("genre_name", genre_in.genre_name).execute()
        if result.data:
            existing = result.data[0]
            return GenreResponseSchema(
                id = existing["genre_id"],
                name = existing["genre_name"],
                info = existing["genre_info"]
            )
        new_genre = supabase_py_service_client.table("Genres").insert({
            "genre_name": genre_in.genre_name,
            "genre_info": genre_in.genre_info
        }).execute()
        return new_genre.data[0]
    except Exception as e:
        print("genre error", e)
        return None

def get_genre(genre_in: GenreCreateSchema = None, genre_name: str = None, genre_id: int = None):
    try:
        query = supabase_py.table("Genres").select("*")
        if genre_in:
            query = query.eq("genre_name", genre_in.genre_name)
        elif genre_name:
            query = query.eq("genre_name", genre_name)
        elif genre_id:
            query = query.eq("genre_id", genre_in.genre_id)
        else:
            return None
        result = query.execute()
        return result.data[0]
    except Exception as e:
        print("Get genre error: ", e)
        return None

def create_genre(genre_in: GenreCreateSchema):
    try:
        if not genre_in:
            return None
        new_genre = supabase_py_service_client.table("Genres").insert({
            "genre_name" : genre_in.genre_name,
            "genre_info" : genre_in.genre_info
        }).execute()
        return new_genre.data[0]
    except Exception as e:
        print("Create genre error: ", e)
        return None

def update_genre(genre_id: int, genre_in: GenreCreateSchema):
    try:
        if not genre_in or not genre_in:
            return None
        update = supabase_py_service_client.table("Genres").update({
            "genre_name": genre_in.genre_name,
            "genre_info": genre_in.genre_info
        }).eq("genre_id", genre_id).execute()

        return update.data[0]
    except Exception as e:
         print ("Update genre error: ", e)
         return None