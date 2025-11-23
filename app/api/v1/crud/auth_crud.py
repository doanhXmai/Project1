from app.core.supabase import supabase_py
from app.schemas.singer_schema import SingerCreateSchema
from uuid import UUID


def get_genre(singer: SingerCreateSchema = None, singer_name: str = None, singer_id: int = None):
    try:
        if singer:
            result = supabase_py.table("Singers").select("*").eq("singer_name", singer.genre_name).execute()
            if result.data:
                return result.data[0]

        if singer_name:
            result = supabase_py.table("Singers").select("*").eq("singer_name", singer_name).execute()
            if result.data:
                return result.data[0]

        result = supabase_py.table("Singers").select("*").eq("singer_id", singer_id).execute()
        if result.data:
            return result.data[0]
    except Exception as e:
        print("get singer error: ", e)
        return None

def get_all_genres():
    try:
        result = supabase_py.table("Genres").select("*")
        row = result.data
        return row
    except Exception as e:
        print("get all genres error: ", e)
        return None

