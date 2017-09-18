from chryso.schema import metadata, table  # pylint: disable=unused-import
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

Track = table('track',
    Column('md5', String(32), nullable=False),
    Column('size', Integer, nullable=False),
)

TrackLocation = table('track_location',
    Column('track', None, ForeignKey('track.uuid'), nullable=False),
    Column('location', String(4096), nullable=False),
)

Build = table('play',
    Column('track', None, ForeignKey('track.uuid'), nullable=False),
    Column('mood', String(1024), nullable=False),
    Column('positive_feedback', Boolean(), nullable=True),
)
