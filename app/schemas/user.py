from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    user_name: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    user_name: Optional[str] = None
    display_name: Optional[str] = None
    role: str
    status: bool

    class Config:
        orm_mode = True