from django.core.cache import cache

from posts.models import Hashtag, Post
from posts.utils.hashtags import extract_hashtags


class PostService:
    @staticmethod
    def create_post(author, title, content, publish_at=None):
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
            publish_at=publish_at,
            is_published=publish_at is None,
        )
        post.hashtags.set((Hashtag.objects.create(name=name) for name in extract_hashtags(content)))
        post.save()
        cache.delete('published_posts')
        return post

    @staticmethod
    def get_published_posts():
        cache_key = 'published_posts'
        posts = cache.get(cache_key)
        if not posts:
            posts = Post.objects.select_related('author').prefetch_related("hashtags").filter(is_published=True).order_by("-published_at")
            cache.set(cache_key, posts, timeout=60 * 15)
        return posts
