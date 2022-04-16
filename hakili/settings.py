import locale
import os
import sys
from pathlib import Path

import environ
from configparser import RawConfigParser
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / 'lib' / 'resources'
LOG_DIR = BASE_DIR.parent / 'logs'

APPS_DIR = BASE_DIR / 'apps'

cfg = RawConfigParser()

env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    # 'dynamic_rest',
    'django_restql',
    'corsheaders',
    'drf_yasg',

    # Third Parts
    'django_filters',
    'versatileimagefield',
    'django_countries',
    'django_extensions',
    'django_seed',

    # Apps
    'apps.user.apps.UserConfig',
    'apps.core.apps.CoreConfig',
    'apps.company.apps.CompanyConfig',
    'apps.stock.apps.StockConfig',
    'apps.finance.apps.FinanceConfig',
    # 'dj_rest_auth'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

ROOT_URLCONF = 'hakili.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hakili.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),

    # 'inventory': env.db_url('MYSQL_URL'),

    """
    'inventory': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    """

    # read os.environ['SQLITE_URL']
    'extra': env.db_url(
        'SQLITE_URL',
        default='sqlite:////{}'.format(BASE_DIR / 'db.sqlite3')
    )
}

"""
CACHES = {
    # Read os.environ['CACHE_URL'] and raises
    # ImproperlyConfigured exception if not found.
    #
    # The cache() method is an alias for cache_url().
    'default': env.cache(),

    # read os.environ['REDIS_URL']
    # 'redis': env.cache_url('REDIS_URL')
}
"""

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = (
    # 'lib.auth_engine.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = "/"

CORS_ALLOWED_ORIGINS = []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

public_root = BASE_DIR.joinpath('public/')
MEDIA_ROOT = public_root / 'media'
MEDIA_URL = env.str('MEDIA_URL', default='/media/')
STATIC_ROOT = public_root / 'static'
STATIC_URL = env.str('STATIC_URL', default='/static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = env.str('LANGUAGE_CODE')
USE_I18N = env.bool('USE_I18N')

# Other configs
APPEND_SLASH = True

LOGIN_URL = '/accounts/login'

LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)

USE_TZ = env.bool('USE_TZ')
TIME_ZONE = env.str('TIME_ZONE')
locale.setlocale(locale.LC_ALL, env.str('LOCALE'))

# Messages

MESSAGE_LEVEL = messages.DEBUG

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# Date & Time settings

TIME_INPUT_FORMATS = [
    '%H:%M',
]

DATE_INPUT_FORMATS = ['%d %B %Y', ]

from .conf import *
