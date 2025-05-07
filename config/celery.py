import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
app = Celery('interview-example')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'publish_post': {
        'task': 'apps.posts.tasks.publish_crontab',
        'schedule':  crontab(minute='*/1')
    },
}
