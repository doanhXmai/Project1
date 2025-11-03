import datetime

from sqlalchemy import BigInteger, DateTime, Identity, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Playlists(Base):
    __tablename__ = 'Playlists'
    __table_args__ = (
        PrimaryKeyConstraint('playlist_id', name='Playlist_pkey'),
        UniqueConstraint('playlist_id', name='Playlist_playlist_id_key')
    )

    playlist_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    playlist_create_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    track: Mapped[list['Tracks']] = relationship('Tracks', secondary='Track_Playlist', back_populates='playlist')
    UserLibrary: Mapped[list['UserLibrary']] = relationship('UserLibrary', back_populates='userLibrary_playlist')
