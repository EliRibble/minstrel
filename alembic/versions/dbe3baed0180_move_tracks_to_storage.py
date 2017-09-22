"""move tracks to storage

Revision ID: dbe3baed0180
Revises: ca0f1c16ecee
Create Date: 2017-09-22 21:37:52.703676

"""

# revision identifiers, used by Alembic.
revision = 'dbe3baed0180'
down_revision = 'ca0f1c16ecee'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql

def upgrade():
    op.execute("UPDATE track_location SET store = (SELECT uuid FROM track_storage)")


def downgrade():
    pass
