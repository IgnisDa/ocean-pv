import os

import dj_database_url

from .base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS =  ['0.0.0.0']
allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
if allowed_hosts:
    ALLOWED_HOSTS += allowed_hosts.split(",")

SECRET_KEY = os.environ.get('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY')

GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('GOOGLE_RECAPTCHA_SITE_KEY')

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
