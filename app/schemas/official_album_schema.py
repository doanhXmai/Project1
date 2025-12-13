from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.config import Settings

settings = Settings()

class OfficialAlbumSchema(BaseModel):
    officialAlbum_singer_id: int
    officialAlbum_name: str
    officialAlbum_info: Optional[str] = None
    officialAlbum_release_date: Optional[datetime] = None
    officialAlbum_uploader_admin_id: Optional[int] = None
    officialAlbum_uploader_user_id: Optional[int] = None
    officialAlbum_target_type: Optional[bool] = True

class OfficialAlbumUpdateSchema(BaseModel):
    officialAlbum_singer_id: int
    officialAlbum_name: str
    officialAlbum_info: Optional[str] = None
    officialAlbum_release_date: Optional[datetime] = None

