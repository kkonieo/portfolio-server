from os import stat

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from apps.project.models import Project


# Create your views here.
class CommentListView(APIView):
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
        if project:
            serializer.save(author=self.request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    """
    댓글 수정, 삭제 API
    """

    def delete(self, request, project_id, comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            return Response(
                {"message": "no comment"}, status=status.HTTP_400_BAD_REQUEST
            )
        comment.delete()
        return Response({"message": "successfully deleted."})

    def put(self, request, project_id, comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if not comment:
            return Response(
                {"message": "no comment"}, status=status.HTTP_400_BAD_REQUEST
            )
        if comment.author != self.request.user:
            return Response(
                {"message": "no authorization"}, status=status.HTTP_401_UNAUTHORIZED
            )
        comment.content = request.data.get("content")
        comment.save()
        return Response({"message": "successfully changed"})
