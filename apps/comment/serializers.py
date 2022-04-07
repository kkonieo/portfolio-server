from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.comment.models import Comment


class CommentSerializer(ModelSerializer):
    author_slug = serializers.CharField(source="author.slug", read_only=True)
    project_id = serializers.IntegerField(source="project.id", read_only=True)

    class Meta:
        model = Comment
        fields = ("author_slug", "content", "project_id")
