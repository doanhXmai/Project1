from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class HistoryLoginAdmin(Base):
    __tablename__ = 'HistoryLoginAdmin'
    __table_args__ = (
        ForeignKeyConstraint(['historyLoginAdmin_admin_id'], ['Admins.admin_id'], name='HistoryLoginAdmin_historyLoginAdmin_admin_id_fkey'),
        PrimaryKeyConstraint('historyLoginAdmin_id', name='HistoryLoginAdmin_pkey'),
        UniqueConstraint('historyLoginAdmin_id', name='HistoryLoginAdmin_historyLoginAdmin_id_key')
    )

    historyLoginAdmin_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    historyLoginAdmin_access_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    historyLoginAdmin_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    historyLoginAdmin_admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    historyLoginAdmin_ip: Mapped[Optional[str]] = mapped_column(Text)
    historyLoginAdmin_device: Mapped[Optional[str]] = mapped_column(Text)

    historyLoginAdmin_admin: Mapped['Admins'] = relationship('Admins', back_populates='HistoryLoginAdmin')
