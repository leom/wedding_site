from fabric.api import local, settings, run, cd, env
from fabric.operations import put
from fabric.contrib.console import confirm

def deploy():
    remote_dir = '%s/flask_env' % env.remote_home
    run('touch %s/tmp/restart.txt' % remote_dir)
    run('source flask_env/bin/activate && pip install -r %s/wedding_site/requirements.txt' % remote_dir)

    put('*.py', '%s/wedding_site' % remote_dir)
    put('*.ini', '%s/wedding_site' % remote_dir)
    put('*.txt', '%s/wedding_site' % remote_dir)
    with cd('%s/wedding_site' % remote_dir):
        run('mkdir -p templates')
        put('templates/*.html', 'templates')

        run('mkdir -p static/bootstrap static/img')
        put('static/bootstrap/*', 'static/bootstrap')
        put('static/img/*', 'static/img')
        put('static/*.css', 'static')
        put('static/*.js', 'static')

        run('mkdir -p migrations')
        put('./migrations/*.py', 'migrations')
        put('./migrations/versions/*.py', 'migrations/versions')
        put('./migrations/*.mako', 'migrations')
