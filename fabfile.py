from fabric.api import local, settings, run, cd, env
from fabric.operations import put
from fabric.contrib.project import rsync_project
from fabric.contrib.console import confirm

def deploy():
    remote_dir = '%s/flask_env' % env.remote_home
    run('source flask_env/bin/activate && pip install -r %s/wedding_site/requirements.txt' % remote_dir)
    run('find %s/flask_env -iname "*.pyc" -exec rm {} \;' % env.remote_home)

    rsync_project(remote_dir='%s/wedding_site' % remote_dir, local_dir='./', delete=True, exclude=['*.pyc', '*.ini', '.*', '*.psd', 'passenger_wsgi.py'])
    put('alembic.ini', remote_dir)
    put('passenger_wsgi.py', remote_dir)

    run('touch %s/tmp/restart.txt' % remote_dir)
