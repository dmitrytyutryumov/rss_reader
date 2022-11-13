.EXPORT_ALL_VARIABLES:
PYTHONPATH=./
POETRY ?= .venv/bin/poetry
API_ROOT_FOLDER = ./src/api

include ./.env

.PHONY: install-packages
install-packages:
	pip install poetry
	poetry install --no-root

.PHONY: fmt
fmt:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run black . --diff
	poetry run isort . --diff
	poetry run flake8 . --config=setup.cfg

.PHONY: test
test:
	poetry run pytest src/api

.PHONY: run-api
run-api:
	ENV
	poetry run python ${API_ROOT_FOLDER}/manage.py runserver localhost:8000

.PHONY: makemigrations
makemigrations:
	poetry run python ${API_ROOT_FOLDER}/manage.py makemigrations

.PHONY: api-server-migrate
migrate:
	poetry run python ${API_ROOT_FOLDER}/manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	poetry run python ${API_ROOT_FOLDER}/manage.py createsuperuser

.PHONY: collectstatic
collectstatic:
	poetry run python ${API_ROOT_FOLDER}/manage.py collectstatic

.PHONY: add_default_rss
add_default_rss:
	poetry run python ${API_ROOT_FOLDER}/manage.py add_default_rss

.PHONY: run-celery
run-celery:
	cd src/api && poetry run celery -A api worker -l INFO -B

.PHONY: docker-up
docker-up:
	docker-compose -f docker/docker-compose.yaml up -d --build

.PHONY: docker-down
docker-down:
	docker-compose -f docker/docker-compose.yaml down

.PHONY: docker-migrate
docker-migrate:
	docker exec -it api poetry run python manage.py migrate

.PHONY: docker-createsuperuser
docker-createsuperuser:
	docker exec -it api poetry run python manage.py createsuperuser

.PHONY: docker-add_default_rss
docker-add_default_rss:
	docker exec -it api poetry run python manage.py add_default_rss
