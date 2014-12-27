# encoding: utf-8

from fabric import colors
from fabric.api import env, local, task

env.run = 'python manage.py'

DEFAULT_PORT = 8000
DEFAULT_DJANGO_SETTINGS_MODULE = 'crawler.settings.local'

@task
def runserver(port=DEFAULT_PORT, settings=DEFAULT_DJANGO_SETTINGS_MODULE):
    local('%s runserver_plus 0.0.0.0:%s --settings=%s' % (env.run, port, settings))


@task
def shell(settings=DEFAULT_DJANGO_SETTINGS_MODULE):
    local('%s shell_plus --settings=%s' % (env.run, settings))