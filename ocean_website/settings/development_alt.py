import os

from decouple import Csv, config

from .base import *  # NOQA

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost")

SECRET_KEY = config("SECRET_KEY", default="")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")

EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)

EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

GOOGLE_RECAPTCHA_SECRET_KEY = config("GOOGLE_RECAPTCHA_SECRET_KEY", default="")

GOOGLE_RECAPTCHA_SITE_KEY = config("GOOGLE_RECAPTCHA_SITE_KEY", default="")

DATABASE_NAME = config("DATABASE_NAME", default="")

DATABASE_USER = config("DATABASE_USER", default="")

DATABASE_PASSWORD = config("DATABASE_PASSWORD", default="")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),  # NOQA
    }
}
