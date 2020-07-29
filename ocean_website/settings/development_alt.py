import os

from decouple import config, Csv

from .base import *  # NOQA

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SECRET_KEY = config('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = config('EMAIL_HOST')

EMAIL_PORT = config('EMAIL_PORT', cast=int)

EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY')

GOOGLE_RECAPTCHA_SITE_KEY = config('GOOGLE_RECAPTCHA_SITE_KEY')

DATABASE_NAME = config('DATABASE_NAME')

DATABASE_USER = config('DATABASE_USER')

DATABASE_PASSWORD = config('DATABASE_PASSWORD')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
