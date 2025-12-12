from datetime import time, datetime
from typing import Optional

from pydantic import BaseModel



class TrackRequestCreateSchema(BaseModel):
    track_title: str
    track_info: Optional[str] = None
    track_duration: Optional[str] = None
    track_lyric: Optional[str] = None
    track_officialAlbum_id: Optional[int] = None
    track_total_view: Optional[int] = 0

class TrackCreateSchema(BaseModel):
    track_title                         : str
    track_info                          : Optional[str]         = None
    track_duration                      : Optional[time]        = None
    track_lyric_url                     : Optional[str]         = None
    track_poster_url                    : Optional[str]         = None
    track_banner_url                    : Optional[str]         = None
    track_audio_url                     : Optional[str]         = None
    track_officialAlbum_id              : Optional[int]         = None
    track_upload_date                   : Optional[datetime]    = None
    track_total_view                    : Optional[int]         = 0

class TrackResponseBannerSchema(BaseModel):
    track_id: int
    track_title: str
    track_banner_url: Optional[str] = None
    track_total_view: Optional[int] = 0

class TrackResponseSchema(BaseModel):
    track_id                            : int
    track_title                         : str
    track_info                          : Optional[str]         = None
    track_duration                      : Optional[time]        = None
    track_lyric_url                     : Optional[str]         = None
    track_poster_url                    : Optional[str]         = None
    track_banner_url                    : Optional[str]         = None
    track_audio_url                     : Optional[str]         = None
    track_officialAlbum_id              : Optional[int]         = None
    track_upload_date                   : Optional[datetime]    = None
    track_total_view                    : Optional[int]         = 0

    class Config:
        from_attributes = True