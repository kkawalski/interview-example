from rest_framework import generics

from posts.serializers import PostSerializer
from posts.services import PostService


class PostListCreateAPI(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return PostService.get_published_posts()

    def perform_create(self, serializer: PostSerializer):
        PostService.create_post(
            author=self.request.user,
            **serializer.validated_data
        )
