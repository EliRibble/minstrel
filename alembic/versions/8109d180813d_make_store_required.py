"""make store required

Revision ID: 8109d180813d
Revises: dbe3baed0180
Create Date: 2017-09-22 21:46:22.423618

"""

# revision identifiers, used by Alembic.
revision = '8109d180813d'
down_revision = 'dbe3baed0180'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.alter_column('track_location', 'store',
               existing_type=postgresql.UUID(),
               nullable=False)


def downgrade():
    op.alter_column('track_location', 'store',
               existing_type=postgresql.UUID(),
               nullable=True)
