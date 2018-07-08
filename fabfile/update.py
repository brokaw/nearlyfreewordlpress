import os
from fabric.api import run, put, task, env
from fabric.contrib.project import rsync_project


def theme_dir_path():
    grandparent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(grandparent_dir, 'themes')

@task(default=True, name='site')
def update_site():
    """
    Update WordPress core, update the database, and update all plugins.
    """
    update_wp()
    update_plugins()

@task(name='wp')
def update_wp():
    """
    Update WordPress core and update the database.
    """
    run('wp core update')
    run('wp core update-db')

@task(name='plugins')
def update_plugins(name=None):
    """
    Update all WordPress plugins.
    """
    if name:
        run('wp plugin update {}'.format(name))
    else:
        run('wp plugin update --all')

@task(name='themes')
def update_themes():
    """
    Syncs the content in the themes folder.
    """
    sync_dir = theme_dir_path() + '/'
    rsync_project(local_dir=sync_dir, remote_dir='/home/public/wp-content/themes/')

def update_uploads():
    rsync_project(local_dir='uploads/', remote_dir='/home/public/wp-content/uploads/')

@task(name='htaccess')
def update_htaccess():
    '''
    Puts the htaccess in the document root, overriding any existing file
    '''
    if os.path.isfile('htaccess'):
        put(local_path='htaccess', remote_path="{}/.htaccess".format(env.WP_DOCUMENT_ROOT))
