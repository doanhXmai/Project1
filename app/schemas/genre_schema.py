from typing import Optional

from pydantic import BaseModel


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

