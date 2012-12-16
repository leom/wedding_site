import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import Integer, Boolean, String, DateTime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', String(256))
    uri = db.Column('uri', String(256), unique=False)
    is_uploaded = db.Column('is_uploaded', Boolean)
    submitter = db.Column('submitter', String(256))
    created = db.Column('created', DateTime)

    def __init__(self, uri, is_uploaded, submitter=None):
        self.uri = uri
        self.is_uploaded = is_uploaded
        self.submitter = None

    def __repr__(self):
        return '<Song[%s] %s submitted by: %>' % (self.id, self.name, self.submitter)
