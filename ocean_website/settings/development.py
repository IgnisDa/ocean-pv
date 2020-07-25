from .base import *  # NOQA


ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True

SECRET_KEY = '316b5cf48f099fb4e95f149c5e844d9a7632803cdc055d29056edcb82dfc8c10'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST_USER = 'ocean-pv_dev@email.com'
