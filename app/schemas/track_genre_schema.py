from pydantic import BaseModel


class TrackGenreLinkSchema(BaseModel):
    track_id: int
    genre_id: int