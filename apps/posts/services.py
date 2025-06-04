import logging

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from rest_framework import exceptions

from apps.posts import models as post_models
from apps.posts.utils import hashtags as hashtags_utils

logger = logging.getLogger(__name__)

CACHE_KEY_PUBLISHED_POSTS = "posts:published"
CACHE_TIMEOUT = settings.CACHE_TIMEOUT_PUBLISHED_POSTS


class PostService:
    @staticmethod
    def create_post(author, title, content, publish_at=None):
        try:
            with transaction.atomic():
                post = post_models.Post.objects.create(
                    author=author,
                    title=title,
                    content=content,
                    publish_at=publish_at,
                    is_published=publish_at is None,
                )

                hashtags = hashtags_utils.extract_hashtags(content)
                hashtag_objs = [
                    post_models.Hashtag.objects.get_or_create(name=name)[0] for name in hashtags
                ]
                post.hashtags.set(hashtag_objs)

                cache.delete(CACHE_KEY_PUBLISHED_POSTS)
                logger.info(f"Пост успешно создан: id={post.id}")

                return post

        except IntegrityError as e:
            logger.exception(f"Ошибка целостности при создании поста: {e}")
            raise exceptions.ValidationError({"detail": "Ошибка целостности данных."})
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при создании поста: {e}")
            raise exceptions.ValidationError({"detail": "Внутренняя ошибка сервиса."})

    @staticmethod
    def get_published_posts():
        posts = cache.get(CACHE_KEY_PUBLISHED_POSTS)
        if posts is None:
            posts = (
                post_models.Post.objects.select_related("author")
                .prefetch_related("posts")
                .filter(is_published=True)
                .order_by("-published_at")
            )
            cache.set(CACHE_KEY_PUBLISHED_POSTS, posts, timeout=CACHE_TIMEOUT)
        return posts
