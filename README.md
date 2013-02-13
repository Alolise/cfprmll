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

So, for debian-based (Debian >= Wheezy, Ubuntu >= Oneiric):

    sudo apt-get install python-django

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
    # If you've dev rights to push changes, use instead:
    # git clone git@github.com:RMLL/cfprmll.git
    cd cfprmll

Build the database:

    python manage.py syncdb

Build the translations:

    python manage.py compilemessages

Launch the dev webserver:

    python manage.py runserver  # to launch the developpement server

Visit it at http://127.0.0.1:8000/

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

Countries data
--------------

By default, you will have the countries data loaded in your database.

If you need to modify the data, it's in data/countries.csv, and you'll need to
run the following command to import it:

    python manage.py import_countries

To update the default data, do this ( **WARNING** this will dump all the data in
the manager app, not only the countries, **do this only if you know what you are
doing**):

    python manage.py dumpdata --format=json manager > manager/fixtures/initial_data.json
