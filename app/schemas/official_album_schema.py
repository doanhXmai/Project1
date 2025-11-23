from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.singer_schema import SingerResponseSchema


class OfficialAlbumCreateSchema(BaseModel):
    officialAlbum_singer_id: int
    officialAlbum_uploader_user_id: UUID

    officialAlbum_name: str
    officialAlbum_release_date: Optional[date] = None
    officialAlbum_info: Optional[str]= None

class OfficialResponseSchema(BaseModel):
    officialAlbum_id: int

    officialAlbum_uploader_user_id: UUID
    singer: SingerResponseSchema

    officialAlbum_name: str
    officialAlbum_release_date: Optional[date] = None
    officialAlbum_info: Optional[str] = None

    class Config:
        from_attributes = True
