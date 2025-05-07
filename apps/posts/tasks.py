from celery import shared_task
from django.utils import timezone

from apps.posts.models import Post


@shared_task
def publish_crontab():
    date_now = timezone.now()
    Post.objects.filter(
        publish_at__lte=date_now,
        is_published=False,
    ).update(
        is_published=True,
        published_at=date_now
    )
