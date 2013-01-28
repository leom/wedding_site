import sys, os
INTERP = os.path.join(os.environ['HOME'], 'flask_env', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)


sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.environ['HOME'], 'flask_env', 'wedding_site'))
from wedding_site.main import app as application

# Uncomment next two lines to enable debugging
from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, evalex=True)
