.EXPORT_ALL_VARIABLES:
PYTHONPATH=./
POETRY ?= .venv/bin/poetry
API_ROOT_FOLDER = ./src/api

include ./.env

.PHONY: fmt
fmt:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run black . --diff
	poetry run isort . --diff
	poetry run flake8 . --config=setup.cfg


.PHONY: api-server
api-server:
	ENV
	poetry run python ${API_ROOT_FOLDER}/manage.py runserver localhost:8000

.PHONY: api-server-migrate
api-server-migrate:
	poetry run python ${API_ROOT_FOLDER}/manage.py migrate

.PHONY: api-server-createsuperuser
api-server-createsuperuser:
	poetry run python ${API_ROOT_FOLDER}/manage.py createsuperuser

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
docker-createuser:
	docker exec -it api poetry run python manage.py createsuperuser
