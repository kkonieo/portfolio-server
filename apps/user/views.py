import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.core.models import Image
from apps.project.models import Project
from apps.project.serializers import ProjectSerializer
from apps.tag.models import Position, Tech
from apps.tag.serializers import PositionSerializer, TechSerializer
from apps.user.models import Career, Education, Link, OtherExperience, User
from apps.user.serializers import (
    CareerSerializer,
    EducationSerializer,
    LinkSerializer,
    OtherExperienceSerializer,
    UserListSerializer,
    UserSerializer,
)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        """
        로그인

        이메일과 비밀번호를 전송하고 refresh, access 토큰값을 요청합니다.
        """
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        """
        로그아웃

        refresh 토큰을 전송하고 token 을 블랙리스트에 추가합니다 (토큰 만료)
        """
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        토큰 갱신

        refresh 토큰을 전송하고 새로운 access 토큰값을 발급받습니다.
        """
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        """
        토큰 유효성 검사

        access 토큰을 전송하여 토큰이 유효한지 체크합니다.
        """
        return super().post(request, *args, **kwargs)


class UserListView(APIView):
    """
    사용자 리스트 관련 REST API 제공
    """

    def get(self, request):
        """
        전체 사용자 리스트 반환 API
        """
        # 쿼리 분석
        page = request.GET.get("page")
        count = request.GET.get("count")
        user_name = request.GET.get("name")
        positions = request.GET.get("position")
        tech = request.GET.get("tech")

        q = Q()
        if user_name:
            q &= Q(name=user_name)

        if positions:
            positions = positions.split()
            positions = (
                Position.objects.filter(name__in=positions)
                .values("users__pk")
                .annotate(count=Count("users__pk"))
                .filter(count=len(positions))
                .values("users__pk")
            )
            all_position_users = list(positions.values_list("users__pk", flat=True))
            print(all_position_users)
            if all_position_users:
                q &= Q(pk__in=all_position_users)
            else:
                return Response(
                    {"error": "Any Position found"}, status=status.HTTP_404_NOT_FOUND
                )

        if tech:
            tech = tech.split()
            tech = (
                Tech.objects.filter(name__in=tech)
                .values("users__pk")
                .annotate(count=Count("users__pk"))
                .filter(count=len(tech))
                .values("users__pk")
            )
            all_tech_users = list(tech.values_list("users__pk", flat=True))

            if all_tech_users:
                q &= Q(pk__in=all_tech_users)
            else:
                return Response(
                    {"error": "Any Tech found"}, status=status.HTTP_404_NOT_FOUND
                )

        users = User.objects.filter(q).distinct()
        if page and count:
            paginator = Paginator(users, count)
            users = paginator.get_page(page)

        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class DeveloperListView(APIView):
    """
    개발자 리스트
    """

    def get(self, request):
        developers = User.objects.filter(is_staff=True)
        serializer = UserListSerializer(developers, many=True)
        return Response(serializer.data)


class UserView(APIView):
    """
    회원 정보 REST API
    """

    parser_classes = (FormParser, MultiPartParser)

    # permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """
        사용자 상세 정보 반환
        """
        user = User.objects.filter(slug=slug).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, slug):
        """
        사용자 정보 업데이트.
        """
        data = request.POST

        user = User.objects.filter(slug=slug).first()

        user_name = data.get("user_name")
        if user_name:
            user.name = user_name

        user_introduction = data.get("user_introduction")
        if user_introduction:
            user.introduction = user_introduction

        expected_salary = data.get("expected_salary")
        if expected_salary:
            user.expected_salary = expected_salary

        hobby = data.get("hobby")
        if hobby:
            user.hobby = hobby

        user_image = request.FILES.get("user_image")
        if user_image:
            user_image = Image(source=user_image)
            user_image.save()
            user.user_image = user_image

            # data["user_image"] = user_image.source

        user_positions = data.get("user_positions")
        if not user_positions:
            return Response(
                {"message": "must contain user_positions!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user_positions = json.loads(user_positions)
            positions = []
            for t in user_positions:
                position_name = t.get("name")
                if not position_name:
                    return Response(
                        {"message": "user_positions must contain name!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    t = Position.objects.filter(name=position_name).first()
                    if not t:
                        return Response(
                            {"message": "invalid position name"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        positions.append(t)
            user.positions.clear()
            for t in positions:
                user.positions.add(t)
            user.save()

        skills = data.get("skills")
        if not skills:
            return Response(
                {"message": "must contain skills!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            skills = json.loads(skills)
            tech = []
            for skill in skills:
                skill_name = skill.get("name")
                if not skill_name:
                    return Response(
                        {"message": "skills must contain name!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    t = Tech.objects.filter(name=skill_name).first()
                    if not t:
                        return Response(
                            {"message": "invalid position name"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        tech.append(t)
            user.tech.clear()
            for t in tech:
                user.tech.add(t)
            user.save()

        projects = data.get("projects")
        if not projects:
            return Response(
                {"message": "must contain projects!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        projects = json.loads(projects)
        project_serializer = ProjectSerializer(data=projects, many=True)
        if project_serializer.is_valid():
            old_projects = Project.objects.filter(author=user)
            old_projects.delete()
            projects = project_serializer.save(author=user)
            for project in projects:
                project_likers = project.liker.all()
                for project_liker in project_likers:
                    project.likers.add(project_liker)
                project_tech_stacks = project.tech_stack.all()
                for project_tech_stack in project_tech_stacks:
                    project.tech_stack.add(project_tech_stack)
                project.save()

        else:
            return Response(
                project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # # user links
        user_links = data.get("user_links")
        if not user_links:
            return Response(
                {"message": "must contain user_links!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_links = json.loads(user_links)
        Link.objects.filter(user=user).delete()
        for user_link in user_links:
            link = Link(source=user_link, user=user)
            link.save()

        # TODO: other_experiences, developed_functions 구현 - 위 project 구현 참고
        careers = data.get("careers")
        if not careers:
            return Response(
                {"message": "must contain careers!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        careers = json.loads(careers)
        career_serializer = CareerSerializer(data=careers, many=True)
        if career_serializer.is_valid():
            old_careers = Career.objects.filter(user=user)
            old_careers.delete()
            careers = career_serializer.save(user=user)
            for career in careers:
                positions = career.positions.all()
                for position in positions:
                    career.positions.add(position)
                career_tech_stacks = career.tech.all()
                for career_tech_stack in career_tech_stacks:
                    career.tech.add(career_tech_stack)
                career.save()

        else:
            return Response(
                career_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        educations = data.get("educations")
        if not educations:
            return Response(
                {"message": "must contain educations!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        educations = json.loads(educations)
        education_serializer = EducationSerializer(data=educations, many=True)
        if education_serializer.is_valid():
            old_educations = Education.objects.filter(user=user)
            old_educations.delete()
            educations = education_serializer.save(user=user)

        else:
            return Response(
                education_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        other_experiences = data.get("other_experiences")
        if not other_experiences:
            return Response(
                {"message": "must contain other_experiences!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        other_experiences = json.loads(other_experiences)
        other_experience_serializer = OtherExperienceSerializer(
            data=other_experiences, many=True
        )
        if other_experience_serializer.is_valid():
            old_other_experience = OtherExperience.objects.filter(user=user)
            old_other_experience.delete()
            other_experiences = other_experience_serializer.save(user=user)
            for other_experience in other_experiences:
                other_experience_tech = other_experience.tech.all()
                for other_experience_t in other_experience_tech:
                    other_experience.tech.add(other_experience_t)
                other_experience.save()

        else:
            return Response(
                other_experience_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
