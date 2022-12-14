#!/usr/bin/bash
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
poetry run gunicorn api.wsgi -b 0.0.0.0:8000 --workers=2 --threads=4
