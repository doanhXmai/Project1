from typing import Optional
import datetime
import uuid

from sqlalchemy import Boolean, CheckConstraint, Computed, DateTime, Double, ForeignKeyConstraint, Identity, Index, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table, Text, Time, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('email_change_confirm_status >= 0 AND email_change_confirm_status <= 2', name='users_email_change_confirm_status_check'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('phone', name='users_phone_key'),
        Index('confirmation_token_idx', 'confirmation_token', unique=True),
        Index('email_change_token_current_idx', 'email_change_token_current', unique=True),
        Index('email_change_token_new_idx', 'email_change_token_new', unique=True),
        Index('reauthentication_token_idx', 'reauthentication_token', unique=True),
        Index('recovery_token_idx', 'recovery_token', unique=True),
        Index('users_email_partial_key', 'email', unique=True),
        Index('users_instance_id_email_idx', 'instance_id'),
        Index('users_instance_id_idx', 'instance_id'),
        Index('users_is_anonymous_idx', 'is_anonymous'),
        {'comment': 'Auth: Stores user login data within a secure schema.',
     'schema': 'auth'}
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    is_sso_user: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='Auth: Set this column to true when the account comes from SSO. These accounts can have duplicate emails.')
    is_anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    instance_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    aud: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    encrypted_password: Mapped[Optional[str]] = mapped_column(String(255))
    email_confirmed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    invited_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    confirmation_token: Mapped[Optional[str]] = mapped_column(String(255))
    confirmation_sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    recovery_token: Mapped[Optional[str]] = mapped_column(String(255))
    recovery_sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    email_change_token_new: Mapped[Optional[str]] = mapped_column(String(255))
    email_change: Mapped[Optional[str]] = mapped_column(String(255))
    email_change_sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    last_sign_in_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    raw_app_meta_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    raw_user_meta_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    is_super_admin: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    phone: Mapped[Optional[str]] = mapped_column(Text, server_default=text('NULL::character varying'))
    phone_confirmed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    phone_change: Mapped[Optional[str]] = mapped_column(Text, server_default=text("''::character varying"))
    phone_change_token: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("''::character varying"))
    phone_change_sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    confirmed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), Computed('LEAST(email_confirmed_at, phone_confirmed_at)', persisted=True))
    email_change_token_current: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("''::character varying"))
    email_change_confirm_status: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'))
    banned_until: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    reauthentication_token: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("''::character varying"))
    reauthentication_sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

class Users_(Users):
    __tablename__ = 'Users'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE', name='Users_user_id_fkey'),
        PrimaryKeyConstraint('user_id', name='Users_pkey'),
        UniqueConstraint('user_email', name='Users_user_email_key'),
        UniqueConstraint('user_id', name='Users_user_id_key'),
        UniqueConstraint('user_name', name='Users_user_name_key'),
        UniqueConstraint('user_phone', name='Users_user_phone_key')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_role: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[Optional[str]] = mapped_column(Text)
    user_display_name: Mapped[Optional[str]] = mapped_column(Text)
    user_info: Mapped[Optional[str]] = mapped_column(Text)
    user_create_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    user_last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    user_password: Mapped[Optional[str]] = mapped_column(Text)
    user_email: Mapped[Optional[str]] = mapped_column(Text)
    user_phone: Mapped[Optional[str]] = mapped_column(Text)
    user_update_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    AdminAction: Mapped[list['AdminAction']] = relationship('AdminAction', back_populates='user')
    FollowingUser: Mapped[list['FollowingUser']] = relationship('FollowingUser', foreign_keys='[FollowingUser.followingUser_followed_user_id]', back_populates='followingUser_followed_user')
    FollowingUser_: Mapped[list['FollowingUser']] = relationship('FollowingUser', foreign_keys='[FollowingUser.followingUser_user_id]', back_populates='followingUser_user')
    HistoryLoginUser: Mapped[list['HistoryLoginUser']] = relationship('HistoryLoginUser', back_populates='historyLoginUser_user')
    Reports: Mapped[list['Reports']] = relationship('Reports', back_populates='report_creator_user')
    report: Mapped[list['Reports']] = relationship('Reports', secondary='User_report', back_populates='user')
    Tracks: Mapped[list['Tracks']] = relationship('Tracks', back_populates='track_uploader_user')
    UserAlbums: Mapped[list['UserAlbums']] = relationship('UserAlbums', back_populates='userAlbum_create_user')
    CommentAlbum: Mapped[list['CommentAlbum']] = relationship('CommentAlbum', back_populates='commentAlbum_user')
    CommentTrack: Mapped[list['CommentTrack']] = relationship('CommentTrack', back_populates='commentTrack_user')
    FollowingTrack: Mapped[list['FollowingTrack']] = relationship('FollowingTrack', back_populates='followingTrack_user')
    FollowingUserAlbum: Mapped[list['FollowingUserAlbum']] = relationship('FollowingUserAlbum', back_populates='followingUserAlbum_user')
    LikeAlbum: Mapped[list['LikeAlbum']] = relationship('LikeAlbum', back_populates='likeAlbum_user')
    LikeTrack: Mapped[list['LikeTrack']] = relationship('LikeTrack', back_populates='likeTrack_user')
    UserLibrary: Mapped[list['UserLibrary']] = relationship('UserLibrary', back_populates='userLibrary_user')