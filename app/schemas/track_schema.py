import uuid
from datetime import time, datetime
from typing import Optional, List

from fastapi import UploadFile, File, Form

from pydantic import BaseModel

from app.schemas.genre_schema import GenreResponseSchema
from app.schemas.official_album_schema import OfficialResponseSchema
from app.schemas.singer_schema import SingerResponseSchema
from app.schemas.user_schema import UserResponseSchema


class TrackCreateSchema(BaseModel):
    title: str
    info: Optional[str] = None
    duration: Optional[time] = None

    singers: List[str]
    genres: List[str]

    official_album_id: int

class TrackResponseSchema(BaseModel):
    track_id: int
    track_title: str
    track_info: Optional[str] = None
    track_duration: Optional[time] = None

    track_lyric_url: Optional[str] = None
    track_poster_url: Optional[str] = None
    track_audio_url: str

    track_uploader_user_id: UserResponseSchema
    official_album: OfficialResponseSchema
    track_upload_date: Optional[datetime] = None

    singers: List[SingerResponseSchema]
    genres: List[GenreResponseSchema]

    class Config:
        from_attributes = True

class TrackListItemSchema(BaseModel):
    id: int
    title: str
    poster_url: Optional[str]
    duration: Optional[time]

    class Config:
        from_attributes = True

class UploadTrackRequest:
    def __init__(self,
                 track_title: str = Form(...),
                 track_poster: UploadFile = File(None),
                 track_info: str = Form(None),
                 track_audio: UploadFile = File(...),
                 track_official_album: str = Form(None)
        ):
        self.track_title = track_title
        self.track_poster = track_poster
        self.track_info = track_info
        self.track_audio = track_audio
        self.track_officialAlbum = track_official_album
