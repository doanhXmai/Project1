from typing import Optional
from sqlalchemy import BigInteger, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Genres(Base):
    __tablename__ = 'Genres'
    __table_args__ = (
        PrimaryKeyConstraint('genre_id', name='Genre_pkey'),
        UniqueConstraint('genre_id', name='Genre_genre_id_key'),
        UniqueConstraint('genre_name', name='Genre_genre_name_key')
    )

    genre_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    genre_name: Mapped[str] = mapped_column(Text, nullable=False)
    genre_info: Mapped[Optional[str]] = mapped_column(Text)

    track: Mapped[list['Tracks']] = relationship('Tracks', secondary='Track_Genre', back_populates='genre')