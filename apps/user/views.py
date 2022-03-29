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

from apps.tag.models import Position, Tech
from apps.user.models import User
from apps.user.serializers import UserListSerializer


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
    회원 정보 등록을 위한 REST API
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_slug = request.data.get("user_slug")
        if not user_slug:
            return Response(
                {"error": "user_slug must be given!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(slug=user_slug).first()

        # user_name = request.data.get("user_name")
        # if not user_name:
        #     return Response(
        #         {"error": "user_name must be given!"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # user.name = user_name

        # user_introduction = request.data.get("user_introduction")
        # if not user_introduction:
        #     return Response(
        #         {"error": "user_introduction must be given!"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # user.introduction = user_introduction

        user_image = request.FILES.get("user_image")

        # 저장돼있는 유저 정보 가져와서 다른 부분만 업데이트 -> put
