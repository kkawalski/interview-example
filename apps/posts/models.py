from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Hashtag(models.Model):
    """
    Represents a hashtag that can be associated with posts.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Hashtag(id={self.id}, name='{self.name}')"


class Post(models.Model):
    """
    Represents a blog or content post with optional hashtags and scheduling.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    publish_at = models.DateTimeField(null=True, db_index=True)
    published_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Post(id={self.id}, title='{self.title}')"

    # 1. class Meta
    # 2. is_published is bool field. I think in most cases Selectivity will wrong.
    # 3. same as is_published. I think in most cases Selectivity will wrong, because we use __lte filter.
    # In my opinion, in 2 and 3 cases postgresql will be use Parallel seq scan
    # https://www.postgresql.org/docs/current/index-cost-estimation.html
    indexes = [
        models.Index(fields=["is_published", "publish_at"]),
    ]
