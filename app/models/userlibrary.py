from typing import Optional
import uuid

from sqlalchemy import BigInteger, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserLibrary(Base):
    __tablename__ = 'UserLibrary'
    __table_args__ = (
        ForeignKeyConstraint(['userLibrary_officialAlbum_id'], ['OfficialAlbums.officialAlbum_id'], ondelete='CASCADE', name='UserLibrary_userLibrary_officialAlbum_id_fkey'),
        ForeignKeyConstraint(['userLibrary_playlist_id'], ['Playlists.playlist_id'], ondelete='CASCADE', name='UserLibrary_userLibrary_playlist_id_fkey'),
        ForeignKeyConstraint(['userLibrary_track_id'], ['Tracks.track_id'], ondelete='CASCADE', name='UserLibrary_userLibrary_track_id_fkey'),
        ForeignKeyConstraint(['userLibrary_userAlbum_id'], ['UserAlbums.userAlbum_id'], ondelete='CASCADE', name='UserLibrary_userLibrary_userAlbum_id_fkey'),
        ForeignKeyConstraint(['userLibrary_user_id'], ['Users.user_id'], ondelete='CASCADE', name='UserLibrary_userLibrary_user_id_fkey'),
        PrimaryKeyConstraint('userLibrary_id', name='UserLibrary_pkey'),
        UniqueConstraint('userLibrary_id', name='UserLibrary_userLibrary_id_key')
    )

    userLibrary_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    userLibrary_target_type: Mapped[int] = mapped_column(BigInteger, nullable=False)
    userLibrary_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    userLibrary_userAlbum_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    userLibrary_officialAlbum_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    userLibrary_track_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    userLibrary_playlist_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    userLibrary_officialAlbum: Mapped[Optional['OfficialAlbums']] = relationship('OfficialAlbums', back_populates='UserLibrary')
    userLibrary_playlist: Mapped[Optional['Playlists']] = relationship('Playlists', back_populates='UserLibrary')
    userLibrary_track: Mapped[Optional['Tracks']] = relationship('Tracks', back_populates='UserLibrary')
    userLibrary_userAlbum: Mapped[Optional['UserAlbums']] = relationship('UserAlbums', back_populates='UserLibrary')
    userLibrary_user: Mapped['Users_'] = relationship('Users_', back_populates='UserLibrary')