import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Statistics(Base):
    __tablename__ = 'Statistics'
    __table_args__ = (
        ForeignKeyConstraint(['statistics_admin_id'], ['Admins.admin_id'], name='Statistics_statistics_admin_id_fkey'),
        PrimaryKeyConstraint('statistics_id', name='Statistics_pkey'),
        UniqueConstraint('statistics_id', name='Statistics_statistics_id_key')
    )

    statistics_id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    statistics_metrics_name: Mapped[str] = mapped_column(Text, nullable=False)
    statistics_metrics_value: Mapped[str] = mapped_column(Text, nullable=False)
    statistics_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    statistics_scope: Mapped[int] = mapped_column(BigInteger, nullable=False)
    statistics_admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    statistics_admin: Mapped['Admins'] = relationship('Admins', back_populates='Statistics')