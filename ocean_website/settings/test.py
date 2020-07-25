from .base import *  # NOQA

SECRET_KEY = '7090cc6b57865d26946447d695ad1cf143eecda36edf05fddcc9774c43ed9e21'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory:",
    }
}


EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
