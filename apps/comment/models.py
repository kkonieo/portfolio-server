from django.conf import settings
from django.db import models

from apps.core.models import TimeStampModel
from apps.project.models import Project


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
    project = models.ForeignKey(
        Project,
        verbose_name="댓글이 속한 프로젝트",
        on_delete=models.CASCADE,
        related_name="comment_project",
    )

    class Meta:
        verbose_name_plural = "댓글"
        db_table = "comment"

    def __str__(self):
        return self.content
