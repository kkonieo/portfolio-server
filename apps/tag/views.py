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
        keyword = request.GET.get("keyword")

        if not keyword:
            tech = Tech.objects.all()
            serializer = TechSerializer(tech, many=True)
            return Response(serializer.data)
        else:
            keyword = keyword.lower()
