from datetime import datetime
from typing import Optional

from uuid import UUID

from pydantic import BaseModel

from app.core.config import Settings

settings = Settings()

class PasswordResetsCreateSchema(BaseModel):
    passwordResets_user_id: UUID
    passwordResets_email: Optional[str] = None
    passwordResets_otp_code: Optional[str] = None
    passwordResets_expired_at: Optional[datetime] = settings.DATE_NOW.isoformat()