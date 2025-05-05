import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
app = Celery('interview-example')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
