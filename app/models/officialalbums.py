from typing import Optional
import datetime

from sqlalchemy import BigInteger, Date, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class OfficialAlbums(Base):
    __tablename__ = 'OfficialAlbums'
    __table_args__ = (
        ForeignKeyConstraint(['officialAlbum_singer_id'], ['Singers.singer_id'], name='OfficialAlbum_officialAlbum_singer_id_fkey'),
        PrimaryKeyConstraint('officialAlbum_id', name='OfficialAlbum_pkey'),
        UniqueConstraint('officialAlbum_id', name='OfficialAlbum_officialAlbum_id_key')
    )

    officialAlbum_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    officialAlbum_singer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    officialAlbum_name: Mapped[str] = mapped_column(Text, nullable=False)
    officialAlbum_release_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    officialAlbum_info: Mapped[Optional[str]] = mapped_column(Text)

    officialAlbum_singer: Mapped['Singers'] = relationship('Singers', back_populates='OfficialAlbums')
    Tracks: Mapped[list['Tracks']] = relationship('Tracks', back_populates='track_officialAlbum')
    UserLibrary: Mapped[list['UserLibrary']] = relationship('UserLibrary', back_populates='userLibrary_officialAlbum')
