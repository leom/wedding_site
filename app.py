import os
from app_util import *
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
        if fp and allowed_file(fp.filename):
            filename = secure_filename(fp.filename)
            fp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    else:
        return render_template('music.html')

@app.route('/music/play/<filename>')
def play_song(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def navlinks():
    return dict(navlinks=[
        ('/', 'Home'),
        ('/venue', 'Venue & Directions'),
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

app.add_url_rule('/venue', view_func=RenderTemplateView.as_view('venue_view', template_name='venue.html'))
app.add_url_rule('/accommodate', view_func=RenderTemplateView.as_view('accommodate_view', template_name='accommodate.html'))
app.add_url_rule('/rsvp', view_func=RenderTemplateView.as_view('rsvp_view', template_name='rsvp.html'))
app.add_url_rule('/london', view_func=RenderTemplateView.as_view('london_view', template_name='london.html'))
app.add_url_rule('/registry', view_func=RenderTemplateView.as_view('registry_view', template_name='registry.html'))
app.add_url_rule('/contact', view_func=RenderTemplateView.as_view('contact_view', template_name='contact.html'))
app.debug = bool(os.environ.get('FLASK_DEBUG', 'False'))
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(app.root_path, 'playme'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0')
