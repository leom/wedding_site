import os
import configparser

class Config(object):
    config = configparser.ConfigParser()
    config.read('alembic.ini')
    DB_URI = conf['alembic']['sqlalchemy.url']
    DEBUG = bool(os.environ.get('FLASK_DEBUG', 'True'))
    TESTING = bool(os.environ.get('FLASK_TESTING', 'True'))
