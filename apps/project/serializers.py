from dataclasses import field
from statistics import mode

from django.utils.html import strip_tags
from django.utils.text import normalize_newlines
from rest_framework import serializers

from apps.core.models import Image
from apps.user.models import User

from .models import Project


class LikerSerializer(serializers.ModelSerializer):
    """
    좋아요 누른 사람 slug, name
    """

    class Meta:
        model = User
        fields = ("slug", "name")


class ProjectSerializer(serializers.ModelSerializer):
    """
    프로젝트
    """

    thumbnail = serializers.ImageField(source="thumbnail.source")
    likers = LikerSerializer(source="liker", many=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "author",
            "title",
            "content",
            "thumbnail",
            "tech_stack",
            "likers",
        )


class ProjectSummarySerializer(ProjectSerializer):
    """
    프로젝트의 제목, 썸네일, 내용(미리보기 내용)
    """

    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        strip_string = strip_tags(obj.content).strip()
        strip_string = normalize_newlines(strip_string)
        strip_string = strip_string.replace("\n", " ")
        return strip_string[:100]

    class Meta(ProjectSerializer.Meta):
        fields = ("id", "title", "thumbnail", "content")
