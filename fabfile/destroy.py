from fabric.api import run, task, env


@task(default=True, name='site')
def destroy_site():
    """
    Drops the database and removes the WordPress files.
    """
    destroy_wp()
    destroy_db()


@task(name='wp')
def destroy_wp():
    """
    Removes the WordPress files.
    """
    run('rm -r {}/*'.format(env.WP_DOCUMENT_ROOT))


@task(name='db')
def destroy_db():
    """
    Drops the WordPress database and removed the database user.
    """
    run('mysqladmin --defaults-file={home}/.my-admin.cnf --force drop {dbname}'.format(
        home=env.HOME, dbname=env.DB_NAME))
    run("mysql --defaults-file={home}/.my-admin.cnf -e 'DROP USER \"{user}\"@\"%\"'".format(
        home=env.HOME, user=env.DB_USER))
