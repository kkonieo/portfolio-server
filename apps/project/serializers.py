from rest_framework import serializers

from .models import Project


class ProjectCardSerializer(serializers.ModelSerializer):
    """
    프로젝트의 제목, 썸네일
    """

    class Meta:
        model = Project
        fields = ("title", "thumbnail")


class ProjectSummarySerializer(serializers.ModelSerializer):
    """
    프로젝트의 제목, 썸네일, 내용
    """

    class Meta:
        model = Project
        fields = ("title", "thumbnail", "content")


class ProjectSerializer(serializers.ModelSerializer):
    """
    프로젝트
    """

    class Meta:
        model = Project
        fields = "__all__"
