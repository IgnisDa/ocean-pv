import os

from .base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = os.environ.get('SECRET_KEY')

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')

EMAIL_HOST = os.environ.get('EMAIL_HOST')

EMAIL_PORT = os.environ.get('EMAIL_PORT')

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY')

GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('GOOGLE_RECAPTCHA_SITE_KEY')
