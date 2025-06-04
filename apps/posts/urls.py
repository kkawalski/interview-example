from django.urls import path

from apps.posts import views


urlpatterns = [
    path('posts/', views.PostView.as_view(), name='post-list-create'),
]
