"""bigger track size

Revision ID: d8e2eeb29dd5
Revises: 65f3243ec6ab
Create Date: 2017-09-18 15:30:13.160409

"""

# revision identifiers, used by Alembic.
revision = 'd8e2eeb29dd5'
down_revision = '65f3243ec6ab'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('track', 'size',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)


def downgrade():
    op.alter_column('track', 'size',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)
