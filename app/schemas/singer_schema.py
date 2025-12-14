from typing import Optional

from pydantic import BaseModel

class SingerRequest(BaseModel):
    singer_name: str
    singer_info: Optional[str] = None

class SingerUpdateRequest(BaseModel):
    singer_id: int
    singer_name: Optional[str] = None
    singer_info: Optional[str] = None
    singer_view: Optional[int] = 0

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

