"""add state

Revision ID: 7efe99eb6e31
Revises: 06d616d13074
Create Date: 2017-09-20 16:17:16.128048

"""

# revision identifiers, used by Alembic.
revision = '7efe99eb6e31'
down_revision = '06d616d13074'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('state',
        sa.Column('mood', sa.String(length=1024), nullable=True)
    )


def downgrade():
    op.drop_table('state')
