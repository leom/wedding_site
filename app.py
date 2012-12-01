import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!'
    pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = bool(os.environ.get('FLASK_DEBUG', 'False'))
    app.run(host='0.0.0.0')

