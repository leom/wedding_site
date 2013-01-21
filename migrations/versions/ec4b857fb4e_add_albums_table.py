"""add albums table

Revision ID: ec4b857fb4e
Revises: fa42b2cc23c
Create Date: 2013-01-21 12:39:03.806278

"""

# revision identifiers, used by Alembic.
revision = 'ec4b857fb4e'
down_revision = 'fa42b2cc23c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'albums',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(128)),
        sa.Column('artist_id', sa.Integer)
    );
    op.create_index('idx_albums_name_artist_id', 'albums', ['artist_id', 'name'])

def downgrade():
    op.drop_index('idx_albums_name_artist_id')
    op.drop_table('albums')
