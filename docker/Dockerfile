FROM python:3.10-slim

ENV ROOT_DIR="/usr/src/app"
ENV PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $ROOT_DIR
RUN mkdir $ROOT_DIR/db

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

COPY docker/run.sh .
RUN chmod +x run.sh

RUN poetry install --only main --no-root

COPY src/api .

EXPOSE 8000

CMD ["bash", "run.sh"]
