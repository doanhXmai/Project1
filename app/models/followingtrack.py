import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class FollowingTrack(Base):
    __tablename__ = 'FollowingTrack'
    __table_args__ = (
        ForeignKeyConstraint(['followingTrack_track_id'], ['Tracks.track_id'], ondelete='CASCADE', name='FollowingTrack_followingTrack_track_id_fkey'),
        ForeignKeyConstraint(['followingTrack_user_id'], ['Users.user_id'], ondelete='CASCADE', name='FollowingTrack_followingTrack_user_id_fkey'),
        PrimaryKeyConstraint('followingTrack_id', name='FollowingTrack_pkey'),
        UniqueConstraint('followingTrack_id', name='FollowingTrack_followingTrack_id_key')
    )

    followingTrack_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    followingTrack_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    followingTrack_track_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    followingTrack_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    followingTrack_track: Mapped['Tracks'] = relationship('Tracks', back_populates='FollowingTrack')
    followingTrack_user: Mapped['Users_'] = relationship('Users_', back_populates='FollowingTrack')