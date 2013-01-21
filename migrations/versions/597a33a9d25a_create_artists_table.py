"""create artists table

Revision ID: 597a33a9d25a
Revises: ec4b857fb4e
Create Date: 2013-01-21 12:41:30.092506

"""

# revision identifiers, used by Alembic.
revision = '597a33a9d25a'
down_revision = 'ec4b857fb4e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'artists',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255))
    )
    op.create_unique_constraint('uq_artist_name', 'artists', ['name'])

def downgrade():
    op.drop_index('uq_artist_name')
    op.drop_table('artists')
