Introduction
============

This is the tool used in 2012 by the RMLL to gather conference propositions..

Installation
============

Dependancies
------------

CFP only needs django to run, so if the package in your distribution is
advanced enough (django 1.3.\* or 1.4.\*), you can use it. For deployement, be
sure to have the lastests version of the current subversion of django for
security reasons.

So, for debian-based (including Ubuntu):

    sudo apt-get install django

If you want to use a virtualenv:

    virtualenv ve
    source ve/bin/activate
    pip install django

To exit the virtualenv:

    deactivate

Usage
-----

Get the sources:

    git clone git://github.com/RMLL/cfprmll.git
    cd cfprmll

Build the database:

    python manage.py syncdb

Build the translations:

    python manage.py compilemessages

Launch the dev webserver:

    python manage.py runserver  # to launch the developpement server

Translation details
===================

To generate/update a .po file you need to do this:

    python manage.py makemessages -v 2 -a -e .html,.txt,.xml

Once you have edited the .po file, you need to generate the .mo by doing this:

    python manage.py compilemessages

Misc
====

If you need to set specific settings, don't modify the settings.py, create a
settings\_local.py and put them in it.
