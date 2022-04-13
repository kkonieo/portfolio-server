from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project
from .serializers import (
    ProjectSerializer,
    ProjectSummarySerializer,
    RawProjectSerializer,
)


class ProjectsView(APIView):
    """
    Project List
    """

    serializer = RawProjectSerializer
    count = 10
    page = 1

    def set_to_show_summary(self, query):
        short = query.get("short")
        if short:
            short = short.lower()

        if short == "true":
            self.serializer = ProjectSummarySerializer

    def set_pagination(self, count, page):
        if count:
            self.count = count
        if page:
            self.page = page

    def interprete_query(self, query):
        self.user_slug = query.get("slug")
        self.set_to_show_summary(query)
        self.set_pagination(query.get("count"), query.get("page"))

    def get(self, request):
        """
        query parameter (option): slug, page, count, short
        slug: slug 전달 시 특정 유저의 프로젝트 반환. 아닐 시 전체 유저 프로젝트 반환. (최신 순)
        page, count: 페이지네이션 원할 시 원하는 페이지와 갯수
        short: true일 경우 프로젝트 요약 정보 반환. 아닐 시 상세 정보 반환.
        """
        self.interprete_query(request.GET)

        # 전체 유저 프로젝트 목록. 최신 순
        if not self.user_slug:
            project_list = Project.objects.order_by("-created_at")

        # 특정 유저 프로젝트 목록 필터링. 최신 순
        else:
            project_list = Project.objects.filter(author__slug=self.user_slug).order_by(
                "-created_at"
            )
        paginator = Paginator(project_list, self.count)
        projects = paginator.get_page(self.page)

        serializer = self.serializer(projects, many=True)

        return Response(serializer.data)


class ProjectView(APIView):
    def get(self, request, project_id):
        """
        특정 프로젝트 조회.
        """
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project)

        return Response(serializer.data)
