#!/usr/bin/env python
import os
import sys


def main():
    if os.environ.get('DJANGO_DEV') == 'True':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'ocean_website.settings.development')
    elif os.environ.get('DJANGO_DEV') == 'False':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'ocean_website.settings.prod')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'ocean_website.settings.development_alt')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
