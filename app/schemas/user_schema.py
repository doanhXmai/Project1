from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserCreateSchema(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_phone: Optional[str] = None
    user_display_name: Optional[str] = None
    user_info: Optional[str] = None
    user_role: str
    user_create_date: Optional[datetime] = None
    user_last_login: Optional[datetime] = None
    user_update_date: Optional[datetime] = None
    user_avatar_url: Optional[str] = None
    user_status: bool

class UserResponseSchema(BaseModel):
    user_id: UUID
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    user_phone: Optional[str] = None
    user_display_name: Optional[str] = None
    user_info: Optional[str] = None
    user_role: str
    user_create_date: Optional[datetime] = None
    user_last_login: Optional[datetime] = None
    user_update_date: Optional[datetime] = None
    user_avatar_url: Optional[str] = None
    user_status: bool

    class Config:
        from_attributes = True

class DisableUserRequest(BaseModel):
    user_id: UUID