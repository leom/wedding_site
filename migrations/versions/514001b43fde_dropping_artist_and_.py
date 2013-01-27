"""dropping artist and albums table, simplifying to just songs (again)

Revision ID: 514001b43fde
Revises: 3f3ac447d00a
Create Date: 2013-01-27 08:39:29.194553

"""

# revision identifiers, used by Alembic.
revision = '514001b43fde'
down_revision = '3f3ac447d00a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ooops.
    op.drop_index('idx_song_created','songs')
    op.drop_table('songs')

    op.drop_index('idx_albums_name_artist_id')
    op.drop_table('albums')

def downgrade():
    raise Exception('Cannot downgrade from this migration')
