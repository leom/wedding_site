import os
from alembic.config import Config

class Config(object):
    cfg = Config(os.path.realpath('alembic.ini'))
    DB_URI = cfg.get_section_option('alembic', 'sqlalchemy.url')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    TESTING = DEBUG
