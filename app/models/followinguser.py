import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class FollowingUser(Base):
    __tablename__ = 'FollowingUser'
    __table_args__ = (
        ForeignKeyConstraint(['followingUser_followed_user_id'], ['Users.user_id'], ondelete='CASCADE', name='FollowingUser_followingUser_followed_user_id_fkey'),
        ForeignKeyConstraint(['followingUser_user_id'], ['Users.user_id'], ondelete='CASCADE', name='FollowingUser_followingUser_user_id_fkey'),
        PrimaryKeyConstraint('followingUser_id', name='FollowingUser_pkey'),
        UniqueConstraint('followingUser_id', name='FollowingUser_followingUser_id_key')
    )

    followingUser_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    followingUser_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    followingUser_followed_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    followingUser_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    followingUser_followed_user: Mapped['Users_'] = relationship('Users_', foreign_keys=[followingUser_followed_user_id], back_populates='FollowingUser')
    followingUser_user: Mapped['Users_'] = relationship('Users_', foreign_keys=[followingUser_user_id], back_populates='FollowingUser_')