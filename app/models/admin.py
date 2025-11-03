from typing import Optional
import datetime

from sqlalchemy import BigInteger, DateTime, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Admins(Base):
    __tablename__ = 'Admins'
    __table_args__ = (
        PrimaryKeyConstraint('admin_id', name='Admin_pkey'),
        UniqueConstraint('admin_email', name='Admin_admin_email_key'),
        UniqueConstraint('admin_id', name='Admin_admin_id_key'),
        UniqueConstraint('admin_name', name='Admins_admin_name_key'),
        UniqueConstraint('admin_phone', name='Admin_admin_phone_key')
    )

    admin_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    admin_role: Mapped[str] = mapped_column(Text, nullable=False)
    admin_name: Mapped[str] = mapped_column(Text, nullable=False)
    admin_password: Mapped[str] = mapped_column(Text, nullable=False)
    admin_display_name: Mapped[str] = mapped_column(Text, nullable=False)
    admin_email: Mapped[str] = mapped_column(Text, nullable=False)
    admin_phone: Mapped[str] = mapped_column(Text, nullable=False)
    admin_create_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    admin_info: Mapped[Optional[str]] = mapped_column(Text)
    admin_last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    HistoryLoginAdmin: Mapped[list['HistoryLoginAdmin']] = relationship('HistoryLoginAdmin', back_populates='historyLoginAdmin_admin')
    Statistics: Mapped[list['Statistics']] = relationship('Statistics', back_populates='statistics_admin')
    AdminAction: Mapped[list['AdminAction']] = relationship('AdminAction', back_populates='admin')
    Reports: Mapped[list['Reports']] = relationship('Reports', back_populates='report_admin')