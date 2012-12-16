import os
import app_util
from flask import Flask, render_template, request
from model import db, app, Song
from werkzeug import secure_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        fp = request.files['file']
        if fp and app_util.allowed_file(fp.filename):
            filename = secure_filename(fp.filename)
            fp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename)
    else:
        return render_template('music.html')

@app.route('/music/play/<filename>')
def play_song(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def navlinks():
    return dict(navlinks=[
        ('/', 'Home'),
        ('/hac', 'Venue & Directions'),
        ('/accommodate', 'Accommodations'),
        ('/rsvp', 'RSVP Details'),
        ('/london', 'London'),
        ('/music', 'The Playlist'),
        ('/registry', 'Registry'),
        ('/contact', 'Contact Us')
    ])

@app.context_processor
def title():
    return dict(title=[x[1] for x in navlinks()['navlinks'] if x[0] == request.path][0])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = bool(os.environ.get('FLASK_DEBUG', 'False'))
    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(app.root_path, 'playme'))
    app.run(host='0.0.0.0')
