import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class AdminAction(Base):
    __tablename__ = 'AdminAction'
    __table_args__ = (
        ForeignKeyConstraint(['admin_id'], ['Admins.admin_id'], ondelete='SET NULL', name='AdminAction_admin_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['Users.user_id'], ondelete='SET NULL', name='AdminAction_user_id_fkey'),
        PrimaryKeyConstraint('admin_id', 'user_id', name='AdminAction_pkey')
    )

    admin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    action_reason: Mapped[str] = mapped_column(Text, nullable=False)
    action_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    admin: Mapped['Admins'] = relationship('Admins', back_populates='AdminAction')
    user: Mapped['Users_'] = relationship('Users_', back_populates='AdminAction')