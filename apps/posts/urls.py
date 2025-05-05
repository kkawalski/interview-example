from django.urls import path

from apps.posts.views import PostListCreateAPI


urlpatterns = [
    path('posts/', PostListCreateAPI.as_view(), name='post-list-create'),
]
