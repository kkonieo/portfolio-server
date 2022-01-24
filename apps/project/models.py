from django.conf import settings
from django.db import models

from apps.core.models import Image, TimeStampModel


class Project(TimeStampModel):
    """
    Project 모델
    """

    title = models.CharField(verbose_name="프로젝트 제목", max_length=40)
    content = models.TextField(verbose_name="프로젝트 내용")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="project_user",
    )
    thumbnail = models.OneToOneField(
        Image, verbose_name="프로젝트 썸네일", on_delete=models.CASCADE
    )
    liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="프로젝트에 좋아요 남긴 사용자들",
        related_name="project_liker",
    )

    # TODO: keywords(기술 스택 해시태그) 추가해야 함.

    class Meta:
        verbose_name_plural = "프로젝트"
        db_table = "project"

    def __str__(self):
        return self.title
