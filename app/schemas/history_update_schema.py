from datetime import datetime
from typing import Optional

from uuid import UUID

from pydantic import BaseModel


class HistoryUpdateCreateSchema(BaseModel):
    historyUpdate_date: Optional[datetime] = None
    historyUpdate_target_type: Optional[bool] = True
    historyUpdate_admin_id: Optional[int] = None
    historyUpdate_user_id: Optional[UUID] = None
    historyUpdate_description: Optional[str] = None
    historyUpdate_genre_id: Optional[int] = None
    historyUpdate_singer_id: Optional[int] = None
    historyUpdate_official_album_id: Optional[int] = None

