from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    publish_at = models.DateTimeField(null=True)
    published_at = models.DateTimeField(null=True)
