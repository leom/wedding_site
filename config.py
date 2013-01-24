import os
from alembic.config import Config

class Config(object):
    if os.path.exists(os.path.expanduser('~/production.ini')):
        ini_target = os.path.expanduser('~/production.ini')
    else:
        ini_target = os.path.realpath('alembic.ini')

    cfg = Config(ini_target)
    SQLALCHEMY_DATABASE_URI = cfg.get_section_option('alembic', 'sqlalchemy.url')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    TESTING = DEBUG
