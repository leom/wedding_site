import os
import time
import base64
from app_util import *
from random import randint
from hsaudiotag import auto
from flask import Flask, render_template, request, flash, redirect, url_for
from model import db, app, Song, Artist, Album
from werkzeug import secure_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playlist/add', methods=['GET', 'POST'])
def playlist_add():
    if request.method == 'POST':
        fp = request.files['media_file']
        if fp:
            if allowed_file(fp.filename):
                filename = secure_filename('%d-%s.%s' % (time.time(), randint(1000, 999999), fp.filename))
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                fp.save(filepath)

                # saved file, now try to get the uploaded info
                audio_file = auto.File(filepath)

                # TODO: confirm song isn't already in the DB first
                return render_template('playlist/confirm_upload.html',
                        filepath=filepath,
                        name=audio_file.title,
                        album=audio_file.album,
                        artist=audio_file.artist,
                        submitter=request.form['submitter']
                )
            else:
                err = '%s and %s' % (', '.join(ALLOWED_EXTENSIONS[:-1]), ALLOWED_EXTENSIONS[-1])
                flash(err, 'error')
    return render_template('playlist/add.html')

@app.route('/playlist/add/confirmed', methods=['POST'])
def playlist_add_confirmed():
    artist = Artist.query.filter_by(name=request.form['artist']).first()
    if artist is None:
        artist = Artist(name=request.form['artist'])

    album = Album.query.filter_by(artist_id=artist.id, name=request.form['album']).first()
    if album is None:
        album = Album(name=request.form['album'])

    try:
        uri = request.form['filepath']
        is_uploaded = False
    except KeyError:
        uri = request.form['youtube_link']
        is_uploaded = True

    s = Song.query.filter_by(uri=uri, album_id=album.id).first()
    if s is None:
        album.songs.append(Song(uri,
            request.form['name'],
            is_uploaded=is_uploaded,
            submitter=request.form['submitter']))
        artist.albums.append(album)
        db.session.add(artist)
        db.session.commit()

    return render_template('playlist/add_confirmed.html', name=request.form['name'])


@app.route('/playlist')
def playlist():
    artists = Artist.query.all()
    return render_template('playlist/landing.html', artists=artists)

@app.route('/playlist/play/<filename>')
def play_music(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def navlinks():
    return dict(navlinks=[
        ('/', 'Home'),
        ('/venue', 'Venue & directions'),
        ('/london', 'London')
    ])

@app.context_processor
def title():
    titles = {
        '/': 'Home',
        '/venue': 'Venue and Directions',
        '/london': 'London',
        '/playlist': 'Playlist',
        '/wedding_list': 'Wedding List'
    }
    base_path = '/%s' % request.path.lstrip('/').split('/')[0]
    return dict(title=titles[base_path])

app.add_url_rule('/venue', view_func=RenderTemplateView.as_view('venue_view', template_name='venue.html'))
app.add_url_rule('/london', view_func=RenderTemplateView.as_view('london_view', template_name='london.html'))
app.add_url_rule('/wedding_list', view_func=RenderTemplateView.as_view('wedding_list_view', template_name='wedding_list.html'));
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(app.root_path, 'playme'))

app.secret_key = os.environ.get('FLASK_SECRET_KEY', '4FWlbReDt9AYliu2ys6bGYnuhO+DLl4zH3edeEJD6bU=')
app.debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='127.0.0.1')
