import os
import time
import base64
from app_util import *
from random import randint
from hsaudiotag import auto
from flask import Flask, render_template, request, flash, redirect, url_for
from model import db, app, Song
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
                fp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                flash('Song successfully saved!', 'success')
            else:
                err = '%s and %s' % (', '.join(ALLOWED_EXTENSIONS[:-1]), ALLOWED_EXTENSIONS[-1])
                flash(err, 'error')

    return render_template('playlist/add.html')

@app.route('/playlist/confirm_upload/<b64filename>')
def playlist_confirm_upload(b64filename):
    filename = base64.b64decode(b64filename)
    audio_file = auto.File(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('playlist/confirm_upload.html', audio_file=audio_file)


@app.route('/playlist')
def playlist():
    return render_template('playlist/landing.html')

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
