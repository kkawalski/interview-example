from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


class PostListCreateAPI(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.none()

    def get_queryset(self):
        return PostService.get_published_posts()

    def perform_create(self, serializer: PostSerializer):
        post = PostService.create_post(
            author=self.request.user,
            **serializer.validated_data
        )
        serializer.instance = post
