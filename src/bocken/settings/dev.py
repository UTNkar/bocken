from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'DJANGO_SECRET',
    default='azzlevclmzxgnv7e0yi+fx1!hah9=r4+s%*wif52^!xq5%spgj'
)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# TODO: is this needed?
BASE_URL = 'http://localhost:8000'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
