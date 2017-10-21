import ConfigParser

from fabric.api import run, task, env, local
from fabric.contrib.project import upload_project, rsync_project
from fabric.contrib.files import upload_template, sed

import create
import destroy
import update

parser = ConfigParser.SafeConfigParser()
parser.read('hosting.cfg')

env.hosts = [parser.get('HOST', 'HOSTNAME')]

env.MYSQL_ADMIN = parser.get('HOST', 'MYSQL_ADMIN')
env.MYSQL_HOST = parser.get('HOST', 'MYSQL_HOST')
env.MYSQL_PASSWORD = parser.get('HOST', 'MYSQL_PASSWORD')

env.DB_NAME = parser.get('SITE', 'DB_NAME')
env.DB_USER = parser.get('SITE', 'DB_USER')
env.DB_PASSWORD = parser.get('SITE', 'DB_PASSWORD')

env.WP_DOCUMENT_ROOT = parser.get('SITE', 'WP_DOCUMENT_ROOT')
env.WP_URL = parser.get('SITE', 'WP_URL')
env.WP_TITLE = parser.get('SITE', 'WP_TITLE')
env.WP_ADMIN = parser.get('SITE', 'WP_ADMIN')
env.WP_ADMIN_PASSWORD = parser.get('SITE', 'WP_ADMIN_PASSWORD')
env.WP_ADMIN_EMAIL = parser.get('SITE', 'WP_ADMIN_EMAIL')
env.WP_THEME_NAME = parser.get('SITE', 'WP_THEME_NAME')
env.WP_PLUGINS = parser.get('SITE', 'WP_PLUGINS').split('\n')
env.WP_EXTRA_PHP = parser.get('SITE', 'WP_EXTRA_PHP')

env.use_ssh_config = True


@task
def backup():
    date = run('date "+%Y%m%dT%H%M%S"')
    run('mkdir -p "$HOME/backup/{}"'.format(date))
    run('wp db export $HOME/backup/{date}/{db}_$(date "+%Y%m%dT%H%M%S").sql'.format(date=date, db=env.DB_NAME))
    run('wp export --dir=$HOME/backup/{date}'.format(date=date))
    run('tar -czf $HOME/backup/{date}/{db}_wp-uploads_$(date "+%Y%m%dT%H%M%S").tar.gz wp-content/uploads'.format(db=env.DB_NAME, date=date))

@task
def status():
    run('wp cli info')
    run('wp core check-update')
    run('wp cron event list')
    run('wp plugin list')
    run('wp theme status {}'.format(env.WP_THEME_NAME))


