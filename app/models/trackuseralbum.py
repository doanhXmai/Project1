import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TrackUserAlbum(Base):
    __tablename__ = 'Track_UserAlbum'
    __table_args__ = (
        ForeignKeyConstraint(['track_id'], ['Tracks.track_id'], name='Track_UserAlbum_track_id_fkey'),
        ForeignKeyConstraint(['userAlbum_id'], ['UserAlbums.userAlbum_id'], name='Track_UserAlbum_userAlbum_id_fkey'),
        PrimaryKeyConstraint('track_id', 'userAlbum_id', name='Track_UserAlbum_pkey')
    )

    track_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    userAlbum_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    add_track_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    track: Mapped['Tracks'] = relationship('Tracks', back_populates='Track_UserAlbum')
    userAlbum: Mapped['UserAlbums'] = relationship('UserAlbums', back_populates='Track_UserAlbum')