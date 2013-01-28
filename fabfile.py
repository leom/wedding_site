from fabric.api import local, settings, run, cd, env
from fabric.operations import put
from fabric.contrib.project import rsync_project
from fabric.contrib.console import confirm

def deploy():
    remote_dir = '%s/flask_env' % env.remote_home
    rsync_project(remote_dir='%s/wedding_site' % remote_dir, local_dir='./', delete=True, exclude=['*.pyc', '*.ini', '.*', '*.psd', 'passenger_wsgi.py', 'playme/*', '*.mp3', '*.m4a'])
    with cd(remote_dir):
        run('find -iname "*.pyc" -exec rm {} \;')
        run('source bin/activate && pip install -r wedding_site/requirements.txt && touch tmp/restart.txt')

def setup_config():
    remote_dir = '%s/flask_env' % env.remote_home
    put('alembic.ini', remote_dir)
    put('passenger_wsgi.py', remote_dir)

def migrate():
    remote_dir = '%s/flask_env' % env.remote_home
    with cd(remote_dir):
        run('source bin/activate && cd wedding_site && alembic -c ~/production.ini upgrade head' )
        run('touch tmp/restart.txt')
