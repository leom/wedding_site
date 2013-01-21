"""add album_id to songs

Revision ID: 3f3ac447d00a
Revises: 597a33a9d25a
Create Date: 2013-01-21 12:44:02.849396

"""

# revision identifiers, used by Alembic.
revision = '3f3ac447d00a'
down_revision = '597a33a9d25a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('songs',
        sa.Column('album_id', sa.Integer)
    )

def downgrade():
    op.drop_column('songs', 'album_id')
