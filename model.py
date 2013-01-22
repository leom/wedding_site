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
    name = db.Column('name', String(255))
    uri = db.Column('uri', String(255), unique=True)
    is_uploaded = db.Column('is_uploaded', Boolean)
    submitter = db.Column('submitter', String(256))
    created = db.Column('created', DateTime)
    album_id = db.Column('album_id', db.ForeignKey('albums.id'))

    def __init__(self, uri, name, is_uploaded=True, album=None, submitter=None):
        self.uri = uri
        self.name = name
        self.is_uploaded = is_uploaded
        self.submitter = submitter
        if album is not None:
            self.album_id = album.id

    def __repr__(self):
        return '<Song[%s] %s submitted by: %s>' % (self.id, self.name, self.submitter)

class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', String(255))
    artist_id = db.Column('artist_id', db.ForeignKey('artists.id'))
    songs = orm.relationship(Song)

    def __init__(self, name, artist=None):
        self.name = name
        if artist is not None:
            self.artist_id = artist.id

    def __repr__(self):
        return '<Album [%s] %s by artist id: %s>' % (self.id, self.name, self.artist_id)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', String(255))
    albums = orm.relationship(Album)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Artist [%s] %s>' % (self.id, self.name)
