from rest_framework import serializers
from apps.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и отображения постов.
    """
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'publish_at', 'author']
        read_only_fields = ['id', 'author']
        extra_kwargs = {
            'publish_at': {'required': False, 'allow_null': True},
        }
