from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    publish_at = serializers.DateTimeField(required=False)
