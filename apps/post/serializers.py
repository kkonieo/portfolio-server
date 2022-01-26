from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.name")
    thumbnail = serializers.ImageField(source="thumbnail.source")

    class Meta:
        model = Post
        fields = ["author", "title", "content", "thumbnail", "liker"]
