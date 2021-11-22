from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET')

ALLOWED_HOSTS = ['.utn.se']

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = '.utn.se'

SESSION_COOKIE_SECURE = True

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
SENTRY_DSN = config('SENTRY_DSN', default='')

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

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
