from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer


# Create your views here.
class CommentView(APIView):
    """
    댓글 API
    """
    def get(self, request, project_id):
        """
        프로젝트의 댓글 목록 조회
        """
        comments = Comment.objects.filter(project=project_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
