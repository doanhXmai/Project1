import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class LikeAlbum(Base):
    __tablename__ = 'LikeAlbum'
    __table_args__ = (
        ForeignKeyConstraint(['likeAlbum_userAlbum_id'], ['UserAlbums.userAlbum_id'], ondelete='CASCADE', name='LikeAlbum_likeAlbum_userAlbum_id_fkey'),
        ForeignKeyConstraint(['likeAlbum_user_id'], ['Users.user_id'], ondelete='CASCADE', name='LikeAlbum_likeAlbum_user_id_fkey'),
        PrimaryKeyConstraint('likeAlbum_id', name='LikeAlbum_pkey'),
        UniqueConstraint('likeAlbum_id', name='LikeAlbum_likeAlbum_id_key')
    )

    likeAlbum_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    likeAlbum_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    likeAlbum_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    likeAlbum_userAlbum_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    likeAlbum_userAlbum: Mapped['UserAlbums'] = relationship('UserAlbums', back_populates='LikeAlbum')
    likeAlbum_user: Mapped['Users_'] = relationship('Users_', back_populates='LikeAlbum')