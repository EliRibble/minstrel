from chryso.schema import metadata, table  # pylint: disable=unused-import
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Index, Integer, String, Table

Track = table('track',
    Column('md5', String(32), nullable=False),
    Column('size', BigInteger, nullable=False),
)
Index('track_key_properties',
    Track.c.md5,
    Track.c.size,
    unique=True,
)

TrackStore = table('track_storage',
    Column('name', String(1024), nullable=False),
)

TrackLocation = table('track_location',
    Column('track', None, ForeignKey('track.uuid'), nullable=False),
    Column('location', String(4096), nullable=False),
    Column('store', None, ForeignKey('track_storage.uuid'), nullable=False),
)

Play = table('play',
    Column('track', None, ForeignKey('track.uuid'), nullable=False),
    Column('mood', String(1024), nullable=False),
    Column('played_seconds', Float(), nullable=False),
    Column('positive_feedback', Boolean(), nullable=True),
    Column('reinforced_at_time', DateTime(), nullable=True),
)

State = Table('state', metadata,
    Column('mood', String(1024), nullable=True),
)
