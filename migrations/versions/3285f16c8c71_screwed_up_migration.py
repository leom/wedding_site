"""screwed up migrations, need to recreate songs table

Revision ID: 3285f16c8c71
Revises: 514001b43fde
Create Date: 2013-01-27 09:18:16.395159

"""

# revision identifiers, used by Alembic.
revision = '3285f16c8c71'
down_revision = '514001b43fde'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('artists')
    op.create_table(
        'songs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(255)),
        sa.Column('uri', sa.Unicode(255)),
        sa.Column('is_uploaded', sa.Boolean()),
        sa.Column('artist', sa.Unicode(255)),
        sa.Column('submitter', sa.Unicode(255)),
        sa.Column('created', sa.DateTime()),
    )
    op.create_index('idx_song_created', 'songs', ['created'])


def downgrade():
    raise Exception('Cannot downgrade from this migration - this resets everything')
    pass
