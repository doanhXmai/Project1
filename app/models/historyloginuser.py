from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class HistoryLoginUser(Base):
    __tablename__ = 'HistoryLoginUser'
    __table_args__ = (
        ForeignKeyConstraint(['historyLoginUser_user_id'], ['Users.user_id'], ondelete='SET NULL', name='HistoryLoginUser_historyLoginUser_user_id_fkey'),
        PrimaryKeyConstraint('historyLoginUser_id', name='HistoryLoginUser_pkey'),
        UniqueConstraint('historyLoginUser_id', name='HistoryLoginUser_historyLoginUser_id_key')
    )

    historyLoginUser_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    historyLoginUser_access_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    historyLoginUser_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    historyLoginUser_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    historyLoginUser_ip: Mapped[Optional[str]] = mapped_column(Text)
    historyLoginUser_device: Mapped[Optional[str]] = mapped_column(Text)

    historyLoginUser_user: Mapped['Users_'] = relationship('Users_', back_populates='HistoryLoginUser')