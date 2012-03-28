# -*- coding: utf-8 -*-
import os

PROJECT_DIR = os.path.dirname(__file__)

# DEVEL SETTINGS
DEVEL = os.environ.has_key('DJANGO_DEVEL')

if DEVEL:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
else:
    DEBUG = False
    TEMPLATE_DEBUG = False

SERVER_EMAIL = 'webmaster@rmll.info'
# ADMINS needs to be a list (a tuple make mail_admins fails)
EMAIL_SUBJECT_PREFIX = '[TRACE] '
ADMINS = (
    ('CFP RMLL/LSM Team', 'kolter@openics.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'cfp2012'               # Or path to database file if using sqlite3.
DATABASE_USER = 'cfp'                   # Not used with sqlite3.
DATABASE_PASSWORD = 'cfp'               # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                      # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

LANGUAGES = [
    (u'en', u'English'),
    (u'fr', u'Français'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR + MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%UBeRvHRI"]DwbF{i%o;oRbnRLTVrB?$Rwj5+=Dcs3.SkMFbvu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
#if DEVEL:
#    MIDDLEWARE_CLASSES += [
#        'debug_toolbar.middleware.DebugToolbarMiddleware',
#    ]

ROOT_URLCONF = 'cfp.urls'

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR + '/templates/',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.markup',
    'django.contrib.sites',
    'cfp.manager',
]
if DEVEL:
#    INSTALLED_APPS += [
#        'debug_toolbar',
#    ]
    INTERNAL_IPS = [
        '127.0.0.1',
        #'82.245.96.113',
    ]

# template processors
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
]

### SESSIONS / COOKIES ###
if DEVEL:
    SESSION_COOKIE_NAME = 'cfp-dev'
else:
    SESSION_COOKIE_NAME = 'cfp'
SESSION_COOKIE_AGE = 10800
SESSION_ENGINE = "django.contrib.sessions.backends.file"


### SPECIFICS
CFP_NOTICE_FROM_EMAIL = 'noreply@rmll.info'
CFP_LIMIT_DATE = '2012-03-31 23:59:59'
CFP_ACCEPT_DATE = '2012-04-15'
