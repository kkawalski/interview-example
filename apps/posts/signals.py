from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.posts.models import Post
from apps.posts.tasks import publish_scheduled_post


@receiver(post_save, sender=Post)
def schedule_post(sender, instance: Post, created: bool, **kwargs):
    if created and instance.publish_at and not instance.is_published:
        publish_scheduled_post.apply_async(
            args=[instance.id],
            eta=instance.publish_at,
        )
