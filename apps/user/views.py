from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework import status
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
from apps.user.models import (
    Career,
    DevelopedFunction,
    Education,
    Link,
    OtherExperience,
    User,
)
from apps.user.serializers import (
    CareerSerializer,
    DevelopedFunctionSerializer,
    EducationSerializer,
    OtherExperienceSerializer,
    UserInfoSerializer,
    UserListSerializer,
    UserRegisterSerializer,
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


class UserRegisterView(APIView):
    """
    회원 가입
    """

    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "wrong data"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user:
            return Response(
                {"message": "email already exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        return Response({"user_slug": user.slug}, status=status.HTTP_201_CREATED)


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

    # permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """
        사용자 상세 정보 반환
        """
        user = User.objects.filter(slug=slug).first()
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request, slug):
        """
        사용자 정보 업데이트.
        """
        user_info = request.data

        user = User.objects.filter(slug=slug).first()
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()

            user_image = user_info.get("user_image")
            if user_image:
                user_image = Image.objects.filter(source=user_image).first()
                user.user_image = user_image

            projects = user_info.get("projects")
            if not projects:
                return Response(
                    {"message": "must contain projects!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if projects:
                project_serializer = ProjectSerializer(data=projects, many=True)
                if project_serializer.is_valid():
                    Project.objects.filter(author=user).delete()
                    new_projects = project_serializer.save(author=user)
                    if projects:
                        for i in range(len(new_projects)):
                            thumbnail = projects[i].get("thumbnail")
                            if thumbnail:
                                thumbnail = Image.objects.filter(
                                    source=thumbnail
                                ).first()
                                new_projects[i].thumbnail = thumbnail
                            images = projects[i].get("images")
                            if images:
                                for image in images:
                                    image = Image.objects.filter(source=image).first()
                                    new_projects[i].images.add(image)
                            new_projects[i].save()
                else:
                    return Response(
                        project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            # user links
            user_links = user_info.get("user_links")
            if user_links:
                Link.objects.filter(user=user).delete()
                for user_link in user_links:
                    link = Link(source=user_link, user=user)
                    link.save()

            careers = user_info.get("careers")
            if careers:
                career_serializer = CareerSerializer(data=careers, many=True)
                if career_serializer.is_valid():
                    Career.objects.filter(user=user).delete()
                    careers = career_serializer.save(user=user)

                else:
                    return Response(
                        career_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            educations = user_info.get("educations")
            if educations:
                education_serializer = EducationSerializer(data=educations, many=True)
                if education_serializer.is_valid():
                    Education.objects.filter(user=user).delete()
                    educations = education_serializer.save(user=user)

                else:
                    return Response(
                        education_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            other_experiences = user_info.get("other_experiences")
            if other_experiences:
                other_experience_serializer = OtherExperienceSerializer(
                    data=other_experiences, many=True
                )
                if other_experience_serializer.is_valid():
                    OtherExperience.objects.filter(user=user).delete()
                    other_experiences = other_experience_serializer.save(user=user)

                else:
                    return Response(
                        other_experience_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            developed_functions = user_info.get("developed_functions")
            if developed_functions:
                developed_function_serializer = DevelopedFunctionSerializer(
                    data=developed_functions, many=True
                )
                if developed_function_serializer.is_valid():
                    DevelopedFunction.objects.filter(user=user).delete()
                    developed_functions = developed_function_serializer.save(user=user)

                else:
                    return Response(
                        developed_function_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            user_info_serializer = UserInfoSerializer(user, data=user_serializer.data)
            if user_info_serializer.is_valid():
                return Response(user_info_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                user_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
