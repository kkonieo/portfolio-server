from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import ProjectSerializer, ProjectSummarySerializer


class BaseProjectsView(APIView):
    """
    Base Project List class
    """

    serializer = ProjectSerializer

    def set_to_show_summary(self, query):
        short = query.get("short")
        if short:
            short = short.lower()

        if short == "true":
            self.serializer = ProjectSummarySerializer

    def interprete_query(self, query):
        self.user_slug = query.get("slug")
        self.set_to_show_summary(query)

    def get(self, request):
        self.interprete_query(request.GET)

        # 특정 유저의 프로젝트 목록 필터링. 최신 순
        projects = Project.objects.filter(author__slug=self.user_slug).order_by(
            "-created_at"
        )
        serializer = self.serializer(projects, many=True)

        return Response(serializer.data)


class ProjectsView(BaseProjectsView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put, delete 함수도 작성


class ProjectsSummaryView(BaseProjectsView):
    """
    Project 요약 리스트

    프로젝트의 제목, 썸네일, 내용
    """

    serializer = ProjectSummarySerializer
