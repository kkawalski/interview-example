import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("interview-example")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# app.conf.worker_prefetch_multiplier = 1
# for the future
# https://docs.celeryq.dev/en/stable/userguide/optimizing.html#prefetch-limits
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-worker_prefetch_multiplier

app.conf.beat_schedule = {
    "publish_post": {
        "task": "apps.posts.tasks.publish_crontab",
        "schedule": crontab(minute="*/1"),
    },
}
