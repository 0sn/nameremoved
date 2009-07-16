# Django settings for nrdj project.

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = BASE_DIR
MEDIA_URL = 'http://static.nameremoved.com'
ADMIN_MEDIA_PREFIX = 'http://static.nameremoved.com/admin/'

# only set TRUE in localsettings
DEBUG = False
TEMPLATE_DEBUG = DEBUG

USE_ETAGS = True

ADMINS = (
    ('Nick Wolfe', 'nradmin@nickwolfe.ca'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Toronto'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False

DATE_FORMAT = "Y m d"
DATETIME_FORMAT = "Y m d H:i"

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "nr_linkmanager.context.navigation.nav",
    "django_sqldebug.context.sqldebug.sqldebug",
)

ROOT_URLCONF = 'nr.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django_chunks',
    'django_bonjour',
    'nr_utils',
    'nr_comics',
    'nr_contributions',
    'nr_linkmanager',
#    'questions',
)

from localsettings import *
