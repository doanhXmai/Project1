from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    phone: str
    name: str
    password: str

class AdminCreateSchema(BaseModel):
    admin_email: EmailStr
    admin_phone: str
    admin_name: str
    admin_display_name: Optional[str] = None
    admin_role: str
    admin_password: str

class AdminResponseSchema(BaseModel):
    admin_id: int
    admin_email: EmailStr
    admin_phone: str
    admin_name: str
    admin_role: str
    admin_display_name: Optional[str] = None
    admin_info: Optional[str] = None
    admin_create_date: Optional[datetime] = None
    admin_last_login: Optional[datetime] = None
    admin_status: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DisableAdminRequest(BaseModel):
    admin_id: int