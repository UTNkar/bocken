"""
Django settings for bocken project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from decouple import config
import sys
import os
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'fontawesome_5',
    'bocken',
    'tailwind',
    'utn_tailwind_theme',
    'mathfilters',
    'django_object_actions',
    'captcha',
    'django_cron'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bocken.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bocken.context_processors.klubbmastare_email'
            ],
        },
    },
]

IS_RUNNING_TEST = 'test' in sys.argv

if IS_RUNNING_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DJANGO_DB_NAME', default='bocken'),
            'USER': config('DJANGO_DB_USER', default='bocken'),
            'PASSWORD': config('DJANGO_DB_PASS', default=''),
            'HOST': config('DJANGO_DB_HOST', default='127.0.0.1'),
            'PORT': config('DJANGO_DB_PORT', default='5432'),
        }
    }

WSGI_APPLICATION = 'bocken.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('sv', _('Swedish')),
    ('en', _('English')),
]

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = 'bocken.Admin'

TAILWIND_APP_NAME = 'utn_tailwind_theme'

COST_PER_MIL_DEFAULT = 20

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.WARNING: 'bg-yellow-300 mb-4 p-4 rounded',
}

KLUBBMASTARE_EMAIL = 'klubbmastare@utn.se'

SERVER_EMAIL = 'admin@utn.se'

EMAIL_SUBJECT_PREFIX = '[Automatic message from bocken journal system] - '

ADMINS = [('KM', KLUBBMASTARE_EMAIL)]

INTERNAL_IPS = [
    "127.0.0.1",
]

CRON_CLASSES = [
    "bocken.cron.DeleteOldReportsCronJob",
]
