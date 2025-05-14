from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author = filters.NumberFilter()
    is_published = filters.BooleanFilter()

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'is_published']


class PostListCreateAPI(generics.ListCreateAPIView):
    """
    API endpoint для создания и получения списка постов.
    
    Поддерживает:
    - Создание новых постов (POST)
    - Получение списка постов с пагинацией (GET)
    - Фильтрацию по заголовку, содержанию, автору и статусу публикации
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filterset_class = PostFilter
    queryset = Post.objects.none()

    def get_queryset(self):
        """
        Возвращает отфильтрованный и оптимизированный queryset постов.
        Использует select_related и prefetch_related для оптимизации запросов.
        """
        queryset = PostService.get_published_posts()
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def perform_create(self, serializer: PostSerializer):
        """
        Создает новый пост с использованием PostService.
        Обрабатывает возможные ошибки при создании.
        """
        try:
            post = PostService.create_post(
                author=self.request.user,
                **serializer.validated_data
            )
            serializer.instance = post
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
