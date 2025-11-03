from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, Double, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, Time, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Tracks(Base):
    __tablename__ = 'Tracks'
    __table_args__ = (
        ForeignKeyConstraint(['track_officialAlbum_id'], ['OfficialAlbums.officialAlbum_id'], ondelete='SET NULL', name='Tracks_track_officialAlbum_id_fkey'),
        ForeignKeyConstraint(['track_uploader_user_id'], ['Users.user_id'], ondelete='SET NULL', name='Tracks_track_uploader_user_id_fkey'),
        PrimaryKeyConstraint('track_id', name='Track_pkey'),
        UniqueConstraint('track_id', name='Track_track_id_key')
    )

    track_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    track_title: Mapped[str] = mapped_column(Text, nullable=False)
    track_upload_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    track_audio_url: Mapped[str] = mapped_column(Text, nullable=False)
    track_poster_url: Mapped[Optional[str]] = mapped_column(Text)
    track_info: Mapped[Optional[str]] = mapped_column(Text)
    track_duration: Mapped[Optional[datetime.time]] = mapped_column(Time)
    track_uploader_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    track_officialAlbum_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    genre: Mapped[list['Genres']] = relationship('Genres', secondary='Track_Genre', back_populates='track')
    playlist: Mapped[list['Playlists']] = relationship('Playlists', secondary='Track_Playlist', back_populates='track')
    singer: Mapped[list['Singers']] = relationship('Singers', secondary='Track_Singer', back_populates='track')
    track_officialAlbum: Mapped[Optional['OfficialAlbums']] = relationship('OfficialAlbums', back_populates='Tracks')
    track_uploader_user: Mapped[Optional['Users_']] = relationship('Users_', back_populates='Tracks')
    CommentTrack: Mapped[list['CommentTrack']] = relationship('CommentTrack', back_populates='commentTrack_track')
    FollowingTrack: Mapped[list['FollowingTrack']] = relationship('FollowingTrack', back_populates='followingTrack_track')
    LikeTrack: Mapped[list['LikeTrack']] = relationship('LikeTrack', back_populates='likeTrack_track')
    Track_UserAlbum: Mapped[list['TrackUserAlbum']] = relationship('TrackUserAlbum', back_populates='track')
    UserLibrary: Mapped[list['UserLibrary']] = relationship('UserLibrary', back_populates='userLibrary_track')