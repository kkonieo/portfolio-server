from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import (
    ProjectCardSerializer,
    ProjectSerializer,
    ProjectSummarySerializer,
)


class BaseProjectList(APIView):
    """
    Base Project List class
    """

    serializer = ProjectSerializer

    def get_user(self):
        return self.request.user

    def get(self, request):
        # TODO: fix temp user to real user
        user = "hmkim199@gmail.com"
        # user = self.get_user()
        projects = Project.objects.filter(author=user).order_by("-created_at")
        serializer = self.serializer(projects, many=True)

        return Response(serializer.data)


class ProjectList(BaseProjectList):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put, delete 함수도 작성


class ProjectCardList(BaseProjectList):
    """
    Project 카드 리스트

    프로젝트의 제목, 썸네일 리스트 최신순으로 반환합니다.
    """

    serializer = ProjectCardSerializer


class ProjectSummaryList(BaseProjectList):
    """
    Project 요약 리스트

    프로젝트의 제목, 썸네일, 내용
    """

    serializer = ProjectSummarySerializer
