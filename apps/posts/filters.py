from django_filters import rest_framework as filters
from apps.posts import models

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    content = filters.CharFilter(lookup_expr="icontains")
    author = filters.NumberFilter()
    is_published = filters.BooleanFilter()

    class Meta:
        model = models.Post
        fields = ["title", "content", "author", "is_published"]
