from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'DJANGO_SECRET',
    default='azzlevclmzxgnv7e0yi+fx1!hah9=r4+s%*wif52^!xq5%spgj'
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
