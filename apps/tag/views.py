from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tag.models import Position, Tech
from apps.tag.serializers import PositionSerializer, TechSerializer


# Create your views here.
class TechView(APIView):
    """
    기술 스택 API
    """

    def get(self, request):
        """
        쿼리 파라미터로 keyword 넘기면 키워드 포함하는 모든 기술 스택 리턴,
        쿼리 파라미터 넘기지 않으면 모든 기술 스택 리턴.
        """
        keyword = request.GET.get("keyword")

        if not keyword:
            tech = Tech.objects.all()
        else:
            tech = Tech.objects.filter(name__icontains=keyword)
            if not tech:
                return Response(
                    {"message": "wrong input"}, status=status.HTTP_400_BAD_REQUEST
                )
        serializer = TechSerializer(tech, many=True)
        return Response(serializer.data)


class PositionView(APIView):
    """
    포지션 API
    """

    def get(self, request):
        """
        쿼리 파라미터로 keyword 넘기면 키워드 포함하는 모든 포지션 리턴,
        쿼리 파라미터 넘기지 않으면 모든 포지션 리턴.
        """
        keyword = request.GET.get("keyword")

        if not keyword:
            position = Position.objects.all()
        else:
            position = Position.objects.filter(name__icontains=keyword)
            if not position:
                return Response(
                    {"message": "wrong input"}, status=status.HTTP_400_BAD_REQUEST
                )
        serializer = PositionSerializer(position, many=True)
        return Response(serializer.data)
