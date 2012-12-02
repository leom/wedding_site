import os
from flask import Flask, render_template, request
from model import db, app, Song

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music')
def music():
    return render_template('music.html')

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
    app.run(host='0.0.0.0')

