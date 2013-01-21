import os
from app_util import *
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
                filename = secure_filename(fp.filename)
                fp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Song successfully saved!', 'success')
            else:
                err = '%s and %s' % (', '.join(ALLOWED_EXTENSIONS[:-1]), ALLOWED_EXTENSIONS[-1])
                flash(err, 'error')

    return render_template('playlist/add.html')

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
    print base_path
    return dict(title=titles[base_path])

app.add_url_rule('/venue', view_func=RenderTemplateView.as_view('venue_view', template_name='venue.html'))
app.add_url_rule('/london', view_func=RenderTemplateView.as_view('london_view', template_name='london.html'))
app.add_url_rule('/wedding_list', view_func=RenderTemplateView.as_view('wedding_list_view', template_name='wedding_list.html'));
app.debug = bool(os.environ.get('FLASK_DEBUG', 'False'))
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(app.root_path, 'playme'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1')
