import os
import re
import time
import base64
import datetime
from echonest import get_from_echonest
from youtube import get_video_info, get_video_id
from app_util import *
from random import randint
from hsaudiotag import auto
from flask import Flask, render_template, request, flash, redirect, url_for
from model import db, app, Song
from werkzeug import secure_filename

yt_re = re.compile('youtube.co(m|\.uk)')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playlist/add', methods=['GET', 'POST'])
def playlist_add():
    if request.method == 'POST':
        if request.files:
            fp = request.files['media_file']
            if fp:
                if allowed_file(fp.filename):
                    filename = secure_filename('%d-%s.%s' % (time.time(), randint(1000, 999999), fp.filename))
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    fp.save(filepath)

                    # saved file, now try to get the uploaded info
                    audio_file = auto.File(filepath)
                    print audio_file.title, audio_file.artist

                    return render_template('playlist/confirm_upload.html',
                            uri=filepath,
                            song_title=audio_file.title,
                            artist=audio_file.artist
                    )
                else:
                    err = '%s and %s' % (', '.join(ALLOWED_EXTENSIONS[:-1]), ALLOWED_EXTENSIONS[-1])
                    flash(err, 'error')
                    return
        else:
            search_term = request.form['search']
            is_yt = yt_re.search(search_term)
            uri = title = artist = None
            if is_yt:
                video_id = get_video_id(search_term)
                title, artist = get_video_info(video_id)
            else:
                title, artist = get_from_echonest(search_term)

            if not title:
                title = search_term.capitalize()

            if not artist:
                artist = 'Unknown'

            return render_template('playlist/confirm_upload.html',
                    uri=search_term,
                    song_title=title,
                    artist=artist
            )

    return render_template('playlist/add.html')

@app.route('/playlist/add/confirmed', methods=['POST'])
def playlist_add_confirmed():
    is_uploaded = yt_re.search(request.form['uri']) == False

    # we'll clean up duplicates manually
    song = Song(uri=request.form['uri'], title=request.form['title'], artist=request.form['artist'])
    song.submitter = request.form['submitter']
    song.is_uploaded = is_uploaded
    song.created = datetime.datetime.now()

    db.session.add(song)
    db.session.commit()
    return render_template('playlist/add_confirmed.html', song=song)


@app.route('/playlist')
def playlist():
    songs = Song.query.all()
    print songs
    return render_template('playlist/landing.html', songs=songs)

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
