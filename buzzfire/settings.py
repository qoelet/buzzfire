# Django settings for buzzfire project.
import sys, os

DEPLOY = 'LOCAL' # 'LOCAL' or 'PRODUCTION'

DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Oh Choon Kee', 'soulofpeace@gmail.com'),
	('Kenny Shen', 'kenny@northpole.sg'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Asia/Singapore'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

if DEPLOY == 'LOCAL':
	# Absolute path to the directory that holds media.
	# Example: "/home/media/media.lawrence.com/"
	MEDIA_ROOT = os.path.abspath('') + '/media/'
	STATIC_DOC_ROOT = MEDIA_ROOT
	# URL that handles the media served from MEDIA_ROOT. Make sure to use a
	# trailing slash if there is a path component (optional in other cases).
	# Examples: "http://media.lawrence.com", "http://example.com/media/"
	MEDIA_URL = '/site_media/'
	TEMPLATE_DIRS = (
	    os.path.abspath('') + '/templates/',
	)
else:
	MEDIA_ROOT = ''
	MEDIA_URL = ''
	TEMPLATE_DIRS = (
	   os.path.abspath('') + '/templates/',
	)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_(%w+hs@vg(orbktzovhc18(s)*ex5@_g)oxe1m&=sxk%a&wgf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'buzzfire.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
	
	# external apps
	'django_extensions',
	
	# buzzfire apps
	'buzzfire.twitter_app',
	'buzzfire.bookmark_app',
	'buzzfire.comment_app',
)

SESSION_ENGINE='django.contrib.sessions.backends.cache'
CACHE_BACKEND = 'buzzfire.redis_cache.cache://localhost:6379'


# Extras
BUZZFIRE_LOGIN_URL = '/login/'
BUZZFIRE_HOME_PAGE = '/'
BUZZFIRE_USER_PAGE = '/mybuzz/'
BUZZ_REDIS_HOST = 'localhost'
BUZZ_REDIS_PORT  = 6379
