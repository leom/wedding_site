"""create songs table

Revision ID: fa42b2cc23c
Revises: None
Create Date: 2012-12-16 16:09:10.350607

"""

# revision identifiers, used by Alembic.
revision = 'fa42b2cc23c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'songs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(128)),
        sa.Column('uri', sa.Unicode(255)),
        sa.Column('is_uploaded', sa.Boolean()),
        sa.Column('submitter', sa.Unicode(255)),
        sa.Column('created', sa.DateTime())
    )
    op.create_unique_constraint('uq_song_name_uri', 'songs', ['name', 'uri'])
    op.create_index('idx_song_created', 'songs', ['created'])


def downgrade():
    op.drop_constraint('idx_song_created')
    op.drop_index('idx_song_created')
    op.drop_table('songs')
