from pydantic import BaseModel


class DefaultSuccessful(BaseModel):
    message: str
    success: bool