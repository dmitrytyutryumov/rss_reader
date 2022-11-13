#!/usr/bin/bash

poetry run python manage.py migrate
poetry run gunicorn api.wsgi -b 0.0.0.0:8000
