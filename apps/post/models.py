import os
import sys
from fileinput import filename
from statistics import mode

from django.db import models

from apps.user.models import User

# Create your models here.


class Post(models.Model):
    """
    Post 모델
    """

    email = models.ForeignKey(
        User, related_name="post_author", on_delete=models.CASCADE
    )

    title = models.CharField(blank=False, max_length=255)

    content = models.TextField(blank=False)

    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class Post_files(Post):
#     """
#     Post files 모델
#     """

#     id = models.ForeignKey(
#         Post.id, related_name="post_files", on_delete=models.CASCADE
#     )  # noqa: E501
#     filename = models.FileField(
#         upload_to=file_upload_path, null=True
#     )  # 어떻게 작성해야 될지 모르겠음..
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)


# class Post_hashtags(Post):
#     """
#     Post hashtags 모델
#     """

#     id = models.ManyToManyField(int(11), auto_created=True)
#     name = models.CharField(max_length=200, null=True)
