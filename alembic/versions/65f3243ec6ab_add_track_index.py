"""add track index

Revision ID: 65f3243ec6ab
Revises: c59f6984550b
Create Date: 2017-09-18 15:28:47.598762

"""

# revision identifiers, used by Alembic.
revision = '65f3243ec6ab'
down_revision = 'c59f6984550b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index(op.f('ix_track_track_key_properties'), 'track', ['md5', 'size'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_track_track_key_properties'), table_name='track')
