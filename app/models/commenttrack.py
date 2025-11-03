from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, Double, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class CommentTrack(Base):
    __tablename__ = 'CommentTrack'
    __table_args__ = (
        ForeignKeyConstraint(['commentTrack_track_id'], ['Tracks.track_id'], ondelete='CASCADE', name='CommentTrack_commentTrack_track_id_fkey'),
        ForeignKeyConstraint(['commentTrack_user_id'], ['Users.user_id'], ondelete='SET NULL', name='CommentTrack_commentTrack_user_id_fkey'),
        PrimaryKeyConstraint('commentTrack_id', name='CommentTrack_pkey'),
        UniqueConstraint('commentTrack_id', name='CommentTrack_commentTrack_id_key')
    )

    commentTrack_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    commentTrack_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    commentTrack_content: Mapped[str] = mapped_column(Text, nullable=False)
    commentTrack_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    commentTrack_track_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    commentTrack_track: Mapped[Optional['Tracks']] = relationship('Tracks', back_populates='CommentTrack')
    commentTrack_user: Mapped[Optional['Users_']] = relationship('Users_', back_populates='CommentTrack')