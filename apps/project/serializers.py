from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    프로젝트
    """

    thumbnail = serializers.ImageField(source="thumbnail.source")

    class Meta:
        model = Project
        fields = "__all__"


class ProjectCardSerializer(ProjectSerializer):
    """
    프로젝트의 제목, 썸네일
    """

    class Meta(ProjectSerializer.Meta):
        fields = ("title", "thumbnail")


class ProjectSummarySerializer(ProjectSerializer):
    """
    프로젝트의 제목, 썸네일, 내용(미리보기 내용)
    """

    class Meta(ProjectSerializer.Meta):
        fields = ("title", "thumbnail", "content")
