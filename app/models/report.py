from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Reports(Base):
    __tablename__ = 'Reports'
    __table_args__ = (
        ForeignKeyConstraint(['report_admin_id'], ['Admins.admin_id'], ondelete='SET NULL', name='Reports_report_admin_id_fkey'),
        ForeignKeyConstraint(['report_creator_user_id'], ['Users.user_id'], ondelete='SET NULL', name='Reports_report_creator_user_id_fkey'),
        PrimaryKeyConstraint('report_id', name='Reports_pkey'),
        UniqueConstraint('report_id', name='Reports_report_id_key')
    )

    report_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    report_target_type: Mapped[str] = mapped_column(Text, nullable=False)
    report_content: Mapped[str] = mapped_column(Text, nullable=False)
    report_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    report_create_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    report_creator_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    report_admin_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    report_admin: Mapped[Optional['Admins']] = relationship('Admins', back_populates='Reports')
    report_creator_user: Mapped[Optional['Users_']] = relationship('Users_', back_populates='Reports')
    user: Mapped[list['Users_']] = relationship('Users_', secondary='User_report', back_populates='report')