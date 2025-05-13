import logging
from celery import shared_task
from django.utils import timezone
from django.db import DatabaseError

from apps.posts.models import Post

logger = logging.getLogger(__name__)


@shared_task
def publish_crontab():
    """
    Публикует все отложенные посты, время которых наступило.
    """
    date_now = timezone.now()

    try:
        updated_count = (
            Post.objects
            .filter(publish_at__lte=date_now, is_published=False)
            .update(is_published=True, published_at=date_now)
        )
        logger.info(f"Опубликовано постов: {updated_count}")
    except DatabaseError as e:
        logger.exception(f"Ошибка при публикации постов: {e}")
