from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
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
from apps.tag.models import Position, Tech
from apps.user.models import User
from apps.user.serializers import UserListSerializer, UserSerializer


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

        user = User.objects.get(slug=slug)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_name = request.data.get("user_name")
        if user_name:
            user.name = user_name

        user_introduction = request.data.get("user_introduction")
        if user_introduction:
            user.introduction = user_introduction

        # user image
        user_image = request.FILES.get("user_image")
        if user_image:
            user_image = Image(source=user_image)
            user_image.save()
            user.user_image = user_image.source

        expected_salary = request.data.get("expected_salary")
        if expected_salary:
            user.expected_salary = expected_salary

        hobby = request.data.get("hobby")
        if hobby:
            user.hobby = hobby

        # user_positions = request.data.get("user_positions")
        # if user_positions:
        #     positions = Position.objects.filter()
        #     user.user_positions = user_positions

        # user links
        # user_links = request.data.get("user_links")
        # user_links = Link

        # TODO: 포지션, 테크는 어떻게 저장하지? Serializer 어떻게 할지 고민.
        serializer = UserSerializer(user)
        return Response(serializer.data)
