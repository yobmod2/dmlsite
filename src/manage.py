#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import dotenv

"""
Run the development server, use the command: python manage.py runserver
Run the production server with Gunicorn: uv run gunicorn dmlsite.wsgi:application
Run the production server with Uvicorn: uv run uvicorn dmlsite.asgi:application
Run the production server with Uvicorn and Gunicorn: uv run
    gunicorn myproject.asgi:application -k uvicorn_worker.UvicornWorker
"""


def main() -> None:
    dotenv.read_dotenv(filename="dmlsite.env")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmlsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
