from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    8. 포스트 페이지에서 보여줄 내용입니다.
    """

    author = serializers.EmailField(source="author.email")
    thumbnail = serializers.ImageField(
        source="thumbnail.source"
    )  # source 는 필드를 채우는데 사용할 속성의 이름입니다.

    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        strip_string = strip_tags(obj.content).strip()
        return strip_string[:120]

    class Meta:
        model = Post
        fields = "__all__"


class PostCardSerializer(PostSerializer):
    """
    3. 메인 페이지에서 카드형태로 보여줄 내용입니다.
    """

    class Meta:
        model = Post
        fields = ("title", "thumbnail", "content")


class PostListSerializer(PostSerializer):
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
