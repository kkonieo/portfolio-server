# APIView를 사용하기 위해 import
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


# Blog의 목록을 보여주는 역할
class PostList(APIView):
    # Blog list를 보여줄 때
    def get(self, request):
        posts = Post.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
