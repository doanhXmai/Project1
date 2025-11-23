from pydantic import BaseModel


class TrackSingerLinkSchema(BaseModel):
    track_id: int
    singer_id: int
