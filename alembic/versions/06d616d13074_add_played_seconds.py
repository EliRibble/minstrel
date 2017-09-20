"""add played seconds

Revision ID: 06d616d13074
Revises: 83a1946ee503
Create Date: 2017-09-20 16:07:41.263907

"""

# revision identifiers, used by Alembic.
revision = '06d616d13074'
down_revision = '83a1946ee503'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('play', sa.Column('played_seconds', sa.Float(), nullable=False))


def downgrade():
    op.drop_column('play', 'played_seconds')
