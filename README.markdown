Nearly Free WordPress
================================

A [Fabric](http://www.fabfile.org) script to set up WordPress on [nearlyfreespeech.net](https://www.nearlyfreespeech.net)

What
----

Nearly Free Speech is a mostly DYI web hosting service. They have instructions on how to set up a It is meant to be something like a command-line "one-click install," following the settings and best practices recommended in the NearlyFreeSpeech FAQ.

How
----
### Prerequesites

1. Fabric.

2. Database Server.


### Set up Fabric

I use a virtualenv.

`pip install fabric`

### Start a MySQL Process

There might be an API for this, but right now it's a manual process. The script will create a new database and a database user for your site, but you need to start a MySQL process manually through the web site.

### Set up configuration file.

hosting.cfg holds all relevant variables. There is an example file to copy. I hope most of the settings are obvious.

### Run commands

`fab -l` gives a list of commnds

    backup
    status
    create           Create new database and install WordPress.
    create.db        Create a new database
    create.site      Create new database and install WordPress.
    create.wp        Installs WordPress using an existing database.
    destroy          Drops the database and removes the WordPress files.
    destroy.db       Drops the WordPress database and removed the database us...
    destroy.site     Drops the database and removes the WordPress files.
    destroy.wp       Removes the WordPress files.
    update           Update WordPress core, update the database, and update a...
    update.htaccess  Puts the htaccess in the document root, overriding any e...
    update.plugins   Update all WordPress plugins.
    update.site      Update WordPress core, update the database, and update a...
    update.themes    Syncs the content in the themes folder.
    update.wp        Update WordPress core and update the database.

If hosting.cfg is properly configured, then `fab create` should result in a fully functional WordPress installation.

Maintenance
-----------

The maintenance features are still in progress. Right now it can update WordPress core and sync your themes if you have them in ./themes. This lets you work on your files locally before pushing them up to the server.

Future
------

The end goal is to have a staging and production environment that are kept in sync. Then you can try out new features on your staging site, and push them up to your production site once you are confident they are correct.
