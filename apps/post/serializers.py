import email
from dataclasses import fields
from email.errors import InvalidMultipartContentTransferEncodingDefect
from fileinput import filename

from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from rest_framework import serializers

from apps.core.models import Image
from apps.post.pagination import PostListPagination

from .models import Post, User


class PostWirteSerializer(serializers.ModelSerializer):

    user_slug = serializers.CharField(source="author.slug", read_only=True)
    thumbnail_path = serializers.CharField()

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    """
    8. 포스트 페이지에서 보여줄 내용입니다.
    """

    user_slug = serializers.CharField(source="author.slug", read_only=True)
    # thumbnail = serializers.ImageField(
    #     source="thumbnail.source"
    # )  # source 는 필드를 채우는데 사용할 속성의 이름입니다.
    content = serializers.SerializerMethodField()

    thumbnail_path = serializers.CharField()
    # get_ <을 붙이고 메소드를 정의하면
    # ex:) get_xxxx
    # xxxx 변수의 값은 get_ 함수의 반환값이 된다.

    def get_content(self, obj):
        # ㅐobj -> post model
        # post model에는 content 필드가 있어요
        # obj.content -> post.content
        # post.content 0~120 길이로 자른값을 반환

        strip_string = strip_tags(obj.content).strip()
        return strip_string[:120]

    class Meta:
        model = Post
        fields = [
            "author",
            "user_slug",
            "thumbnail_path",
            "title",
            "content",
            "thumbnail",
        ]
        read_only_fields = ("author", "thumbnail")

    def create(self, validated_data):

        # image = Image.objects.filter(source=validated_data["thumbnail_path"]).first()
        post = Post.objects.create(
            title=validated_data["title"], content=validated_data["content"]
        )

        return post


class PostCardSerializer(serializers.ModelSerializer):
    """
    3. 메인 페이지에서 카드형태로 보여줄 내용입니다.
    """

    class Meta:
        model = Post
        fields = ("title", "thumbnail", "content")


class PostListSerializer(serializers.ModelSerializer):
    """
    4. 프로젝트 소개 페이지에서 리스트(나열) 형태로 보여줄 내용입니다.
    """

    class Meta:
        model = Post
        fields = ("title", "thumbnail", "content")


# class PostWriteSerializer(PostSerializer):

#     def
#     class Meta:
#         model = Post
#         fields = "__all__"
