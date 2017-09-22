"""add default storage

Revision ID: ca0f1c16ecee
Revises: 2b0f6152e206
Create Date: 2017-09-22 21:35:15.650224

"""

# revision identifiers, used by Alembic.
revision = 'ca0f1c16ecee'
down_revision = '2b0f6152e206'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    track_storage = sa.table('track_storage',
        sa.Column('name', sa.String()),
    )
    op.bulk_insert(track_storage, [{'name': 'cloud'}])

def downgrade():
    pass
