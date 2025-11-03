import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class LikeTrack(Base):
    __tablename__ = 'LikeTrack'
    __table_args__ = (
        ForeignKeyConstraint(['likeTrack_track_id'], ['Tracks.track_id'], ondelete='CASCADE', name='LikeTrack_likeTrack_track_id_fkey'),
        ForeignKeyConstraint(['likeTrack_user_id'], ['Users.user_id'], ondelete='CASCADE', name='LikeTrack_likeTrack_user_id_fkey'),
        PrimaryKeyConstraint('likeTrack_id', name='LikeTrack_pkey'),
        UniqueConstraint('likeTrack_id', name='LikeTrack_likeTrack_id_key')
    )

    likeTrack_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    likeTrack_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    likeTrack_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    likeTrack_track_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    likeTrack_track: Mapped['Tracks'] = relationship('Tracks', back_populates='LikeTrack')
    likeTrack_user: Mapped['Users_'] = relationship('Users_', back_populates='LikeTrack')