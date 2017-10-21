Nearly Free WordPress
================================

A [Fabric](http://www.fabfile.org) script to set up WordPress on [nearlyfreespeech.net](https://www.nearlyfreespeech.net)

What
----
Nearly Free Speech is a mostly DYI web hosting service. Their primary support options are FAQ, a wiki, and a member's forum. In return, you get a hosting bargain. It can be a great deal if you know your way around the UNIX shell.

Personally, I feel this tradeoff is worth it. It does take some time to get a site up and running. The permissions aren't wide open and there are some setup steps that aren't common among the WordPress community, so it can be hard to find help with some problems. This script tries to make the steup automatic and follow the best practices from NearlyFreeSpeech.NET.

How
----

TBD.

### Set up Fabric

I use a virtualenv.

`pip install fabric`

### Set up configuration file.

hosting.cfg holds all relevant variables.

### Run commands

`fab -l` gives a list of commnds
