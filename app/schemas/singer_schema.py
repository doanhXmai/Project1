from typing import Optional

from pydantic import BaseModel

from app.core.supabase import supabase_py

class SingerRequest(BaseModel):
    singer_name: str
    singer_info: Optional[str] = None

class SingerUpdateRequest(BaseModel):
    singer_id: int
    singer_name: Optional[str] = None
    singer_info: Optional[str] = None
    singer_view: Optional[str] = 0

class SingerCreateSchema(BaseModel):
    singer_name: str
    singer_info: Optional[str] = None
    singer_view: Optional[str] = 0

class SingerResponseSchema(BaseModel):
    singer_id: int
    singer_name: str
    singer_view: int = 0
    singer_info: Optional[str] = None

    class Config:
        from_attributes = True

def id_to_singer_schema(singer_id: int):
    try:
        result = supabase_py.table("Singer").select("*").eq("singer_id", singer_id).single().execute()
        row = result.data
        return SingerResponseSchema(**row)
    except Exception as e:
        print("id to singer scheme error: ", e)
        return None