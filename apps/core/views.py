from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Image


# Create your views here.
class ImageView(APIView):
    """
    이미지 API
    """

    def post(self, request):
        image = request.FILES.get("image")
        if image:
            image = Image(source=image)
            image.save()
            print(image)
            return Response(
                {"image_source": image.source.name},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
