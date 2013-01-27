import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import Integer, Boolean, String, DateTime
from sqlalchemy import orm

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column('id', Integer, primary_key=True)
    title = db.Column('title', String(255))
    uri = db.Column('uri', String(255), unique=True)
    is_uploaded = db.Column('is_uploaded', Boolean)
    submitter = db.Column('submitter', String(256))
    created = db.Column('created', DateTime)
    artist = db.Column('artist', String(1048))

    def __init__(self, uri, title, is_uploaded=True, artist=None, submitter=None):
        self.uri = uri
        self.title = title
        self.is_uploaded = is_uploaded
        self.submitter = submitter
        self.artist = artist

    def __repr__(self):
        return '<Song[%s] %s by %s submitted by: %s>' % (self.id, self.title, self.artist, self.submitter)
