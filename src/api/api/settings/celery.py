import os

CELERY_BROKER_URL = (
    f"amqp://"
    f"{os.environ['MQ_USER']}:"
    f"{os.environ['MQ_PASSWORD']}"
    f"@{os.environ['MQ_HOST']}:"
    f"{os.environ['MQ_PORT']}"
)
