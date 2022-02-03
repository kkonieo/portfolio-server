# APIView를 사용하기 위해 import
from email.mime import image
from re import search

from django.forms.models import model_to_dict
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.models import Post
from apps.post.pagination import PostListPagination
from apps.post.serializers import (PostCardSerializer, PostCreateSerializer,
                                   PostListSerializer, PostWriteSerializer,)


# Post의 목록을 보여주는 역할
class PostList(APIView, PostListPagination):

    # Post list를 보여줄 때
    def get(self, request):
        """
        포스트 리스트(소개) 조회 뷰
        """
        posts = Post.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정

        posts = self.paginate_queryset(posts, request, view=self)
        serializer = PostListSerializer(posts, many=True)
        return self.get_paginated_response(serializer.data)

    # 새로운 Post 글을 작성할 때
    def post(self, request):
        """
        포스트 생성 뷰
        """
        # request.data는 사용자의 입력 데이터
        print("1 - acting")
        serializer = PostCreateSerializer(data=request.data)
        print("2 - acting")
        if serializer.is_valid():
            print("3.1 - acting")
            serializer.save()
            print("3.2 - acting")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("4 - acting")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Post의 detail을 보여주는 역할
class PostDetail(APIView):
    # Post 객체 가져오기
    def get_object(self, pk):
        """
        post 객체 가져오기
        """
        return get_object_or_404(Post, pk=pk)

    # Post의 detail 보기
    def get(self, request, pk, format=None):
        """
        post 디테일 뷰
        """
        post = self.get_object(pk)
        serializer = PostWriteSerializer(post)
        return Response(serializer.data)

    # Post 수정하기
    def put(self, request, pk, format=None):
        """
        post 수정 뷰
        """
        post = self.get_object(pk)
        serializer = PostWriteSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Post 삭제하기
    def delete(self, request, pk, format=None):
        """
        post 삭제 뷰
        """
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostList(APIView):
#     """
#     4. 프로젝트 소개 페이지에서 리스트(나열) 형태로 뿌려주는 로직입니다.
#     """

#     # Post list를 보여줄 때

#     # permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         posts = Post.objects.all()
#         # 여러 개의 객체를 serialization하기 위해 many=True로 설정

#         serializer = PostSerializer(posts, many=True)  # 시리얼라이즈화한 객체
#         return Response(serializer.data)


# class PostRead(APIView):
#     """
#     8. 포스트 페이지에서 작성된 글의 전체 내용을 보여주는 로직입니다.
#     """

#     def get(self, request, post_id):
#         post = Post.objects.filter(Post, pk=post_id)
#         serializer = PostSerializer(post, many=True)  # 시리얼라이즈화한 객체
#         return Response(serializer.data)


# class PostCreate(APIView):
#     """
#     10. 에디터 페이지에서 게시글 작성시 Post DB 에서 저장되는 로직입니다.
#     """

#     def post(self, request, post_id):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request, post_id):
#         atuhor = self.get_user()
#         post = get_object_or_404(Post, pk=post_id)

#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         validated_data = serializer.validated_data

#         post = Post()
#         post.author = author
#         post.title = validated_data["title"]
#         post.content = validated_data["content"]
#         post.thumbnail = validated_data["thumbnail"]

#         post.save()

#         return Response({"detail": "게시글이 생성되었습니다."}, status=status.HTTP_201_CREATED)


# class PostUD(APIView):
#     def put(self, request, post_id):
#         """
#         10. 에디터 페이지에서 게시글 수정시 Post DB 에서 수정되는 로직입니다.
#         """
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = PostSerializer(data=request.data)

#         if serializer.is_valid(raise_exception=True):  # raise_exception 찾아보기
#             serializer.save()

#         validated_data = serializer.validated_data

#         post.title = validated_data["title"]
#         post.thumbnail = validated_data["thumbnail"]

#         post.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, post_id):
#         """
#         10. 에디터 페이지에서 게시글 수정시 Post DB 에서 삭제되는 로직입니다.
#         """

#         post = get_object_or_404(Post, pk=post_id)
#         post.is_deleted = True
#         post.save()
#         return Response({"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)


# To do : 게시글 create 기능 만들기

# To do : 8. 게시글 상세 페이지에서 update 기능 만들기

# To do : 8. 게시글 상세 페이지에서 delete 기능 만들기 https://naon.me/posts/til56

# # 포스팅 내용, 수정, 삭제
# class PostDetail
# class Posting(APIView):

#     def post(self, request):
#         email = User.objects.get(user_id = login_session)
#         board =


""" PUT 요청 흐름-  - -
1. 요청 받은 데이터 유효한지 검증 is_valid()
2. 요청받은 식별자(id)를 통해 객체가 존재하는지 체크
3. 요청받은 데이터를 통해 불러온 객체를 수정
ex:) 
data = serializer.validation_data
post.content = data["content"]
....(수정)
post.save()
4. 끝!



"""
# 포스트 상세정보
# 포스트 생성
# 포스트 수정 <id>

# 포스트 리스트 ( 요약 )
