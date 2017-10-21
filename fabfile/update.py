import os
from fabric.api import run, task, env, local
from fabric.contrib.project import rsync_project
from .utilities import theme_dir_path


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
def update_plugins():
    """
    Update all WordPress plugins.
    """
    run('wp plugin update --all')

@task(name='content')
def update_theme():
    """
    Syncs the content in the themes folder.
    """
    sync_dir = theme_dir_path() + '/'
    rsync_project(local_dir=sync_dir, remote_dir='/home/public/wp-content/themes/')

def update_uploads():
    rsync_project(local_dir='uploads/', remote_dir='/home/public/wp-content/uploads/')
