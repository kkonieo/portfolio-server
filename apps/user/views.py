from unicodedata import name

from django.core.paginator import Paginator
from django.shortcuts import render
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

        users = User.objects.all()
        if user_name:
            users = users.filter(name=user_name)

        if positions:
            positions = positions.split("+")
            positions = Position.objects.filter(name__in=positions)
            users = users.filter(position__in=User.positions__name)

        if tech:
            tech = tech.split("+")
            tech = Tech.objects.filter(name__in=tech)
            users = users.filter(tech__in=User.tech__name)

        if page and count:
            paginator = Paginator(users, count)
            users = paginator.get_page(page)

        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
