from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET')

# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails. Don't include '/admin' or a
# trailing slash
BASE_URL = 'https://bocken.utn.se'

ALLOWED_HOSTS = ['.utn.se']

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = '.utn.se'

SESSION_COOKIE_SECURE = True
