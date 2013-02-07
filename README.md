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

    git clone git://github.com/RMLL/cfprmll.git
    cd cfprmll
    python manage.py syncdb
    python manage.py runserver  # to launch the developpement server


Misc
====

If you need to set specific settings, don't modify the settings.py, create a
settings\_local.py and put them in it.
