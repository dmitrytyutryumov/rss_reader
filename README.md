# RSS reader
[Requirements](docs/RSS_reader.pdf)

## Description
The project collects RSS feeds and show collected.

## How to prepare the project
`base.env` file consists of settings for the project.

Copy it -- `cat base.env > .env`.

Fill the env vars.
Please, verify settings before running.

(if needed) import postman [collection](docs/postman_collection.json)

## How to run

### Docker run
1. Install docker and docker-compose https://docs.docker.com/engine/install/
2. Start project `make docker-up`
3. (Wait for Postgres) Run migration `make docker-migrate`
4. Create superuser `make docker-createsuperuser`
5. Add default rss feeds `make docker-add_default_rss`
6. Stop the project `make docker-down`

### Local run
1. install [pyenv](https://github.com/pyenv/pyenv#installation)
2. Install [poetry](https://python-poetry.org/docs/#installation)
3. Install python 3.10.* `pyenv install 3.10.2`
4. Install dependencies `poetry install`
5. Comment out `api, celery` sections in `docker-compose.yaml` file.
6. Start docker services `make docker-up`

Run services
1. Prepare db and static files `make migrate collectstatic createsuperuser`
2. Run api service `make run-api`
3. Run celery service `make run-celery`

## Development
1. Install [pre-commit](https://pre-commit.com/#install)
2. Add pre-commit hook `pre-commit install`
3. Install hooks `pre-commit run`

Run code formatting `make fmt`

Run code linters `make lint`
