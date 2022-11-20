release: python manage.py migrate --noinput
web: DJANGO_DEV=False gunicorn ocean_website.wsgi --log-file -

