import os

from celery import Celery
from celery.schedules import crontab
from kombu import Queue

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

app = Celery("rss_app")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# app.conf.task_queues = (
#     Queue('rss_tasks', routing_key='rss.#'),
# )
app.conf.beat_schedule = {
    "rss_feed": {
        "task": "rss.tasks.update_rss_feeds",
        "schedule": crontab(minute="*/1"),
        "args": (16, 16),
    },
}
app.conf.timezone = "UTC"
