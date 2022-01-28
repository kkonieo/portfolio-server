from django.utils.html import strip_tags
from django.utils.text import normalize_newlines
from rest_framework import serializers

from apps.user.models import User

from .models import Project


class LikerSerializer(serializers.ModelSerializer):
    """ """

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
        fields = ("title", "content", "thumbnail", "likers")


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
        fields = ("title", "thumbnail", "content")
