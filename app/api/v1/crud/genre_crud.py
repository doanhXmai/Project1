from app.core.supabase import supabase_py
from app.schemas.genre_schema import GenreCreateSchema


def get_genre(genre: GenreCreateSchema = None, genre_name: str = None, genre_id: int = None):
    try:
        if genre:
            result = supabase_py.table("Genres").select("*").eq("genre_name", genre.genre_name).execute()
            if result.data:
                return result.data[0]

        if genre_name:
            result = supabase_py.table("Genres").select("*").eq("genre_name", genre_name).execute()
            if result.data:
                return result.data[0]

        result = supabase_py.table("Genres").select("*").eq("genre_id", genre_id).execute()
        if result.data:
            return result.data[0]

    except Exception as e:
        print("get genre error: ", e)
        return None