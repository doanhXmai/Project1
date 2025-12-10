from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.genre_schema import GenreCreateSchema, GenreResponseSchema

from uuid import UUID

from app.services.history_update_service import create_history


def get_or_create_genre(user_id: UUID, genre_in: GenreCreateSchema):
    try:
        existing = get_genre(genre_in=genre_in)

        if existing:
            return existing

        return create_genre(genre_in)
    except Exception as e:
        print("genre error", e)
        return None

def get_genre(target_id, genre_in: GenreCreateSchema = None, genre_name: str = None, genre_id: int = None, is_admin: bool = False):
    try:
        query = supabase_py.table("Genres").select("*")
        if genre_in:
            query = query.eq("genre_name", genre_in.genre_name)
        elif genre_name:
            query = query.eq("genre_name", genre_name)
        elif genre_id:
            query = query.eq("genre_id", genre_id)
        else:
            return None

        result = query.execute()

        create_history({"genre_id": result.data[0]["genre_id"]}, target_id, ["Get genre"], is_admin)

        return result.data[0] if result.data else None

    except Exception as e:
        print("Get genre error: ", e)
        return None

def create_genre(user_id: UUID, genre_in: GenreCreateSchema):
    try:
        new_genre = supabase_py_service_client.table("Genres").insert({
            "genre_name": genre_in.genre_name,
            "genre_info": genre_in.genre_info
        }).execute()

        create_history({"genre_id": new_genre.data[0]}, user_id, ["Create genre"], False)

        return new_genre.data[0] if new_genre.data else None

    except Exception as e:
        print("Create genre error:", e)
        return None

def update_genre(genre_id: int, genre_in: GenreCreateSchema):
    try:
        if not genre_in or not genre_in:
            return None

        existing = get_genre(genre_in=genre_in)

        if not existing:
            return None

        update_data = {
            "genre_name": genre_in.genre_name,
            "genre_info": genre_in.genre_info
        }

        update = supabase_py_service_client.table("Genres").update(update_data).eq("genre_id", genre_id).execute()

        return update.data[0] if update.data else None

    except Exception as e:
         print ("Update genre error: ", e)
         return None