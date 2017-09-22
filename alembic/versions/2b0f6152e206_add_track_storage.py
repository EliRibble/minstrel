"""add track storage

Revision ID: 2b0f6152e206
Revises: efdd5be8b4f8
Create Date: 2017-09-22 21:33:19.183845

"""

# revision identifiers, used by Alembic.
revision = '2b0f6152e206'
down_revision = 'efdd5be8b4f8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('track_storage',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=1024), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_track_storage'))
    )
    op.add_column('track_location', sa.Column('store', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(op.f('fk_track_location_track_storage_store'), 'track_location', 'track_storage', ['store'], ['uuid'])

def downgrade():
    op.drop_constraint(op.f('fk_track_location_track_storage_store'), 'track_location', type_='foreignkey')
    op.drop_column('track_location', 'store')
    op.drop_table('track_storage')
