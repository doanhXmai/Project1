from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKeyConstraint, Numeric, PrimaryKeyConstraint, Table, Text, Uuid
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)

t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)

t_Track_Genre = Table(
    'Track_Genre', Base.metadata,
    Column('track_id', BigInteger, primary_key=True),
    Column('genre_id', BigInteger, primary_key=True),
    ForeignKeyConstraint(['genre_id'], ['Genres.genre_id'], ondelete='CASCADE', name='Track_Genre_genre_id_fkey'),
    ForeignKeyConstraint(['track_id'], ['Tracks.track_id'], ondelete='CASCADE', name='Track_Genre_track_id_fkey'),
    PrimaryKeyConstraint('track_id', 'genre_id', name='Track_Genre_pkey')
)

t_Track_Playlist = Table(
    'Track_Playlist', Base.metadata,
    Column('track_id', BigInteger, primary_key=True),
    Column('playlist_id', BigInteger, primary_key=True),
    ForeignKeyConstraint(['playlist_id'], ['Playlists.playlist_id'], name='Track_Playlist_playlist_id_fkey'),
    ForeignKeyConstraint(['track_id'], ['Tracks.track_id'], name='Track_Playlist_track_id_fkey'),
    PrimaryKeyConstraint('track_id', 'playlist_id', name='Track_Playlist_pkey')
)

t_Track_Singer = Table(
    'Track_Singer', Base.metadata,
    Column('track_id', BigInteger, primary_key=True),
    Column('singer_id', BigInteger, primary_key=True),
    ForeignKeyConstraint(['singer_id'], ['Singers.singer_id'], name='Track_Singer_singer_id_fkey'),
    ForeignKeyConstraint(['track_id'], ['Tracks.track_id'], name='Track_Singer_track_id_fkey'),
    PrimaryKeyConstraint('track_id', 'singer_id', name='Track_Singer_pkey')
)

t_User_report = Table(
    'User_report', Base.metadata,
    Column('user_id', Uuid, primary_key=True),
    Column('report_id', BigInteger, primary_key=True),
    ForeignKeyConstraint(['report_id'], ['Reports.report_id'], name='User_report_report_id_fkey'),
    ForeignKeyConstraint(['user_id'], ['Users.user_id'], name='User_report_user_id_fkey'),
    PrimaryKeyConstraint('user_id', 'report_id', name='User_report_pkey')
)
