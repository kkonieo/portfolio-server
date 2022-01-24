from django.conf import settings
from django.db import models

from apps.core.models import TimeStampModel
from apps.post.models import Post


class Comment(TimeStampModel):
    """
    Comment 모델
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="댓글 작성자",
        on_delete=models.CASCADE,
        related_name="comment_author",
    )
    content = models.TextField(verbose_name="댓글 내용")
    post = models.ForeignKey(
        Post,
        verbose_name="댓글이 속한 포스트",
        on_delete=models.CASCADE,
        related_name="comment_post",
    )

    class Meta:
        verbose_name_plural = "댓글"
        db_table = "comment"

    def __str__(self):
        return self.content
