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
    name = db.Column('name', String(255))
    uri = db.Column('uri', String(255), unique=True)
    is_uploaded = db.Column('is_uploaded', Boolean)
    submitter = db.Column('submitter', String(256))
    created = db.Column('created', DateTime)
    album_id = db.Column('album_id', Integer)

    def __init__(self, uri, is_uploaded, submitter=None):
        self.uri = uri
        self.is_uploaded = is_uploaded
        self.submitter = None

    def __repr__(self):
        return '<Song[%s] %s submitted by: %>' % (self.id, self.name, self.submitter)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Artist [%s] %s>' % (self.id, self.name)

class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', String(255))
    artist_id = db.Column('artist_id', Integer)

    def __init__(self, name, artist):
        self.name = name
        self.artist_di = artist.id

    def __repr__(self):
        return '<Album [%s] %s by artist id: %s>' % (self.id, self.name, self.artist_id)

