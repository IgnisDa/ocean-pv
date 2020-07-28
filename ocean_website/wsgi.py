import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ocean_website.settings.heroku')

application = get_wsgi_application()
