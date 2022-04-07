from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from apps.project.models import Project


# Create your views here.
class CommentView(APIView):
    """
    댓글 API
    """
    def get(self, request, project_id):
        """
        프로젝트의 댓글 목록 조회
        """
        project = Project.objects.filter(id=project_id).first()
        comments = Comment.objects.filter(project=project)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        """
        댓글 등록
        """
        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        project = Project.objects.filter(id=project_id).first()
        print(project)
        if project:
            serializer.save(author=self.request.user, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
