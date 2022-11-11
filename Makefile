.EXPORT_ALL_VARIABLES:
PYTHONPATH=./
POETRY ?= $(HOME)/.poetry/bin/poetry

.PHONY: fmt
fmt:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run black . --diff
	poetry run isort . --diff
	poetry run flake8 . --config=setup.cfg

.PHONY: create-local-db
create-local-db:
	mkdir -p ./api_service/db

.PHONY: api-server
api-server: create-local-db
	poetry run python api_service/manage.py runserver localhost:8000

.PHONY: api-server-migrate
api-server-migrate: create-local-db
	poetry run python api_service/manage.py migrate

.PHONY: api-server-createsuperuser
api-server-createsuperuser:
	poetry run python api_service/manage.py createsuperuser

.PHONY: stock-server
stock-server:
	poetry run python stock_service/manage.py runserver localhost:8001

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
