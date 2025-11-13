from typing import Optional

from sqlalchemy import BigInteger, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Singers(Base):
    __tablename__ = 'Singers'
    __table_args__ = (
        PrimaryKeyConstraint('singer_id', name='Singer_pkey'),
        UniqueConstraint('singer_id', name='Singer_singer_id_key')
    )

    singer_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    singer_name: Mapped[str] = mapped_column(Text, nullable=False)
    singer_info: Mapped[Optional[str]] = mapped_column(Text)

    track: Mapped[list['Tracks']] = relationship('Tracks', secondary='Track_Singer', back_populates='singer')
    OfficialAlbums: Mapped[list['OfficialAlbums']] = relationship('OfficialAlbums', back_populates='officialAlbum_singer')
