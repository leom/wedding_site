from flask import render_template
from flask.views import View
ALLOWED_EXTENSIONS = set(['mp3', 'mp4', 'wav', 'm4a', 'ogg'])

def allowed_file(filename):
    global ALLOWED_EXTENSIONS
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class RenderTemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name
    def dispatch_request(self):
        return render_template(self.template_name)

