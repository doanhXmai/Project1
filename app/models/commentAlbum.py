from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class CommentAlbum(Base):
    __tablename__ = 'CommentAlbum'
    __table_args__ = (
        ForeignKeyConstraint(['commentAlbum_userAlbum_id'], ['UserAlbums.userAlbum_id'], ondelete='CASCADE', name='CommentAlbum_commentAlbum_userAlbum_id_fkey'),
        ForeignKeyConstraint(['commentAlbum_user_id'], ['Users.user_id'], ondelete='SET NULL', name='CommentAlbum_commentAlbum_user_id_fkey'),
        PrimaryKeyConstraint('commentAlbum_id', name='CommentAlbum_pkey'),
        UniqueConstraint('commentAlbum_id', name='CommentAlbum_commentAlbum_id_key')
    )

    commentAlbum_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    commentAlbum_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    commentAlbum_content: Mapped[str] = mapped_column(Text, nullable=False)
    commentAlbum_userAlbum_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    commentAlbum_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    commentAlbum_userAlbum: Mapped['UserAlbums'] = relationship('UserAlbums', back_populates='CommentAlbum')
    commentAlbum_user: Mapped[Optional['Users_']] = relationship('Users_', back_populates='CommentAlbum')