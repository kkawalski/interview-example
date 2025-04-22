from django.contrib.admin import ModelAdmin, register

from apps.posts.models import Post, Hashtag


@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    raw_id_fields = ['author']


@register(Hashtag)
class HashtagAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
