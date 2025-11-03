from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserAlbums(Base):
    __tablename__ = 'UserAlbums'
    __table_args__ = (
        ForeignKeyConstraint(['userAlbum_create_user_id'], ['Users.user_id'], name='UserAlbum_userAlbum_create_user_id_fkey'),
        PrimaryKeyConstraint('userAlbum_id', name='UserAlbum_pkey'),
        UniqueConstraint('userAlbum_id', name='UserAlbum_userAlbum_id_key')
    )

    userAlbum_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    userAlbum_create_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    userAlbum_title: Mapped[str] = mapped_column(Text, nullable=False)
    userAlbum_release_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    userAlbum_description: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    userAlbum_type: Mapped[Optional[str]] = mapped_column(Text)

    userAlbum_create_user: Mapped['Users_'] = relationship('Users_', back_populates='UserAlbums')
    CommentAlbum: Mapped[list['CommentAlbum']] = relationship('CommentAlbum', back_populates='commentAlbum_userAlbum')
    FollowingUserAlbum: Mapped[list['FollowingUserAlbum']] = relationship('FollowingUserAlbum', back_populates='followingUserAlbum_userAlbum')
    LikeAlbum: Mapped[list['LikeAlbum']] = relationship('LikeAlbum', back_populates='likeAlbum_userAlbum')
    Track_UserAlbum: Mapped[list['TrackUserAlbum']] = relationship('TrackUserAlbum', back_populates='userAlbum')
    UserLibrary: Mapped[list['UserLibrary']] = relationship('UserLibrary', back_populates='userLibrary_userAlbum')
