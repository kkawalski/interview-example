from celery import shared_task
from django.utils import timezone

from posts.models import Post


@shared_task
def publish_scheduled_post(post_id):
    post = Post.objects.get(id=post_id)
    if not post.is_published and post.publish_at <= timezone.now():
        post.is_published = True
        post.published_at = timezone.now()
        post.save()
