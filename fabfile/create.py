import os

from fabric.api import run, task, cd, env
from fabric.contrib.project import upload_project, rsync_project
from fabric.contrib.files import upload_template


def template_path(filename=''):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'templates', filename)


def install_wp():
    run('mkdir -p /home/private/.wp-cli')
    path = template_path('wp-cli.yml.tmpl')
    upload_template(path, '/home/private/.wp-cli/config.yml', {'path': env.WP_DOCUMENT_ROOT})
    run('wp core download --locale=en_US')
    run('wp core config --dbhost={dbhost} --dbname={dbname} '
        '--dbuser={dbuser} --dbpass={dbpass} --extra-php <<< "{extra_php}"'.format(dbhost=env.MYSQL_HOST, dbname=env.DB_NAME,
        dbuser=env.DB_USER, dbpass=env.DB_PASSWORD, extra_php=env.WP_EXTRA_PHP))
    run('chmod 644 wp-config.php')
    run('wp core install --url={url} --title="{title}" --admin_user={admin_user} '
        '--admin_password={admin_password} --admin_email={admin_email}'.format(
            url=env.WP_URL, title=env.WP_TITLE, admin_user=env.WP_ADMIN,
            admin_password=env.WP_ADMIN_PASSWORD, admin_email=env.WP_ADMIN_EMAIL))


def install_plugins():
    for plugin in env.WP_PLUGINS:
        run('wp plugin install {}'.format(plugin))
    if 'hyper-cache' in env.WP_PLUGINS:
        hypercache()

def htaccess():
    if os.path.isfile('htaccess'):
        put(local_path='htaccess', remote_path="{}/.htaccess".format(env.WP_DOCUMENT_ROOT))

def hypercache():
    run('chmod 775 wp-content')
    run('chgrp web wp-content')
    run('mkdir -p wp-content/cache')
    run('chgrp web wp-content/cache')
    run('chmod 775 wp-content/cache')
    run('mkdir -p wp-content/cache/hyper-cache')
    run('chgrp web wp-content/cache/hyper-cache')
    run('chgrp web wp-content/plugins/hyper-cache/*.php')

def fix_upload_permissions():
    run('mkdir -p wp-content/uploads')
    run('chgrp -R web wp-content/uploads')
    run('chmod -R 775 wp-content/uploads')

def upload_themes():
    upload_project('themes', '/home/public/wp-content/themes')
    upload_project('themes', '/home/public/wp-content/themes')

@task(default=True, name='site')
def create_site():
    """
    Create new database and install WordPress.
    """
    create_db()
    create_wp()

@task(name='wp')
def create_wp():
    """
    Installs WordPress using an existing database.
    """
    install_wp()
    fix_upload_permissions()
    install_plugins()
    upload_themes()

@task(name='db')
def create_db():
    """
    Create a new database
    """
    template = template_path('my.cnf.tmpl')
    db_context = {'user': env.MYSQL_ADMIN,'host': env.MYSQL_HOST, 'password': env.MYSQL_PASSWORD}
    upload_template(template, '/home/private/.my-admin.cnf', context=db_context)
    db_context = {'user': env.DB_USER,'host': env.MYSQL_HOST, 'password': env.DB_PASSWORD}
    upload_template(template, '/home/private/.my.cnf')

    run('mysqladmin --defaults-file=$HOME/.my-admin.cnf create {dbname}'.format(dbname=env.DB_NAME))
    run("mysql --defaults-file=$HOME/.my-admin.cnf -e 'CREATE USER \"{user}\"@\"%\" IDENTIFIED BY "
        "\"{password}\"'".format(user=env.DB_USER, password=env.DB_PASSWORD));
    grant = "SELECT,INSERT,UPDATE,DELETE,CREATE,ALTER,INDEX,DROP,CREATE TEMPORARY TABLES,"\
            "SHOW VIEW,CREATE ROUTINE,ALTER ROUTINE,EXECUTE,CREATE VIEW,EVENT,TRIGGER,"\
            "LOCK TABLES,REFERENCES"
    run("mysql --defaults-file=$HOME/.my-admin.cnf -e 'GRANT {grant} ON "
        "{dbname} . * TO \"{user}\"@\"%\"'".format(dbname=env.DB_NAME, user=env.DB_USER, grant=grant))
