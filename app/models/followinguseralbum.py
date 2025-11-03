import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class FollowingUserAlbum(Base):
    __tablename__ = 'FollowingUserAlbum'
    __table_args__ = (
        ForeignKeyConstraint(['followingUserAlbum_userAlbum_id'], ['UserAlbums.userAlbum_id'], ondelete='CASCADE', name='FollowingUserAlbum_followingUserAlbum_userAlbum_id_fkey'),
        ForeignKeyConstraint(['followingUserAlbum_user_id'], ['Users.user_id'], ondelete='CASCADE', name='FollowingUserAlbum_followingUserAlbum_user_id_fkey'),
        PrimaryKeyConstraint('followingUserAlbum_id', name='FollowingUserAlbum_pkey'),
        UniqueConstraint('followingUserAlbum_id', name='FollowingUserAlbum_followingUserAlbum_id_key')
    )

    followingUserAlbum_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    followingUserAlbum_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    followingUserAlbum_userAlbum_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    followingUserAlbum_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    followingUserAlbum_userAlbum: Mapped['UserAlbums'] = relationship('UserAlbums', back_populates='FollowingUserAlbum')
    followingUserAlbum_user: Mapped['Users_'] = relationship('Users_', back_populates='FollowingUserAlbum')