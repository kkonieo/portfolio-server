import email
from fileinput import filename

from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from rest_framework import serializers

from apps.core.models import Image

from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    8. 포스트 페이지에서 보여줄 내용입니다.
    """

    print("1.1 - acting")
    author = User.objects.get(email="admin@naver.com")
    print(f"{author}")
    author = serializers.CharField(source=f"{author}")
    print(f"{author}")

    print("1.2 - acting")

    thumbnail = Image.objects.first()
    thumbnail = serializers.ImageField(source=f"{thumbnail}")
    print(f"{thumbnail}")
    # source 는 필드를 채우는데 사용할 속성의 이름입니다.

    print("1.3 - acting")
    content = serializers.SerializerMethodField()
    print(f"{content}")
    print("1.4 - acting")

    # def get_content(self, obj):
    #     strip_string = strip_tags(obj.content).strip()
    #     return strip_string[:120]

    class Meta:
        model = Post
        fields = ["author", "title", "content", "thumbnail"]

    def create(self, validated_data):

        return Post.objects.create(**validated_data)


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
