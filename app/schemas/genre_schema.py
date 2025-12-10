from typing import Optional

from pydantic import BaseModel

from app.core.supabase import supabase_py

class GenreRequest(BaseModel):
    genre_name: str
    genre_info: Optional[str] = None

class GenreUpdateRequest(BaseModel):
    genre_id: int
    genre_name: Optional[str] = None
    genre_info: Optional[str] = None

class GenreCreateSchema(BaseModel):
    genre_name: str
    genre_info: Optional[str] = None

class GenreResponseSchema(BaseModel):
    genre_id: int
    genre_name: str
    genre_info: Optional[str] = None

    class Config:
        from_attributes = True

def id_to_genre_schema(genre_id: int):
    try:
        result = supabase_py.table("Genre").select("*").eq("genre_id", genre_id).single().execute()
        row = result.data
        return GenreResponseSchema(**row)
    except Exception as e:
        print("id to genre scheme error: ", e)
        return None

