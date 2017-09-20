"""add single state row

Revision ID: efdd5be8b4f8
Revises: 7efe99eb6e31
Create Date: 2017-09-20 16:22:59.677201

"""

# revision identifiers, used by Alembic.
revision = 'efdd5be8b4f8'
down_revision = '7efe99eb6e31'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    state = sa.table('state',
        sa.Column('mood', sa.String()),
    )
    op.bulk_insert(state, [{'mood': ''}])

def downgrade():
    pass
