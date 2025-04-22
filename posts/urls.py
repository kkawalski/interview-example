from django.urls import path

from posts.views import PostListCreateAPI


urlpatterns = [
    path('posts/', PostListCreateAPI.as_view(), name='post-list-create'),
]
