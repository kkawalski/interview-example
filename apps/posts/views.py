from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from apps.posts import filters as post_filters
from apps.posts import serializers as post_serializers
from apps.posts import services  as post_services


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostView(generics.ListCreateAPIView):
    """
    API endpoint для создания и получения списка постов.

    Поддерживает:
    - Создание новых постов (POST)
    - Получение списка постов с пагинацией (GET)
    - Фильтрацию по заголовку, содержанию, автору и статусу публикации
    """

    serializer_class = post_serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filterset_class = post_filters.PostFilter

    def get_queryset(self):
        """
        Возвращает отфильтрованный и оптимизированный queryset постов.
        Использует select_related и prefetch_related для оптимизации запросов.
        """
        queryset = post_services.PostService.get_published_posts()
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def perform_create(self, serializer: post_serializers.PostSerializer):
        """
        Создает новый пост с использованием PostService.
        Обрабатывает возможные ошибки при создании.
        """
        try:
            post = post_services.PostService.create_post(
                author=self.request.user, **serializer.validated_data
            )
            serializer.instance = post
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
