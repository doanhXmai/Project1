from pydantic import BaseModel

class GetTrackRequest(BaseModel):
    name: str