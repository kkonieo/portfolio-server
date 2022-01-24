from django.db import models

from apps.core.models import Image, TimeStampModel
from apps.user.models import User

# Create your models here.


class Post(TimeStampModel):
    """
    Post 모델
    """

    email = models.ForeignKey(
        User, related_name="post_author", on_delete=models.CASCADE, verbose_name="이메일"
    )

    title = models.CharField(max_length=255, verbose_name="제목")

    content = models.TextField(verbose_name="내용")

    thumbnail = models.OneToOneField(
        Image, on_delete=models.CASCADE, verbose_name="썸네일이미지"
    )

    liker = models.ManyToManyField(
        User, blank=True, related_name="post_liker", verbose_name="좋아요누른사람"
    )

    class Meta:
        verbose_name_plural = "게시글"
        db_table = "post"

    def __str__(self):
        return self.title
