from django.conf import settings
from django.db import models

from apps.core.models import DurationModel, Image, TimeStampModel
from apps.tag.models import Tech
from apps.user.models import User


class Project(TimeStampModel, DurationModel):
    """
    Project 모델
    """

    """
    request body
    {
        "title": "제목",
        "content": "내용",
        "thumbnail": "/media/ffewfewafaewfeaw_image.jpg",
        "tech_stack": [
            1,
            52
        ] # tech pk 넣기
    }
    # view or serializer 에서 직접 처리
    project.author = self.request.user

    liker ( read_only )
    """

    title = models.CharField(verbose_name="프로젝트 제목", max_length=40)
    content = models.TextField(verbose_name="프로젝트 내용")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="프로젝트 작성자",
        on_delete=models.CASCADE,
        related_name="project_author",
    )
    thumbnail = models.OneToOneField(
        Image,
        verbose_name="프로젝트 썸네일",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    images = models.ManyToManyField(
        Image,
        verbose_name="프로젝트 이미지",
        related_name="project_image",
        null=True,
        blank=True,
    )
    liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="프로젝트에 좋아요 남긴 사용자들",
        related_name="project_liker",
        null=True,
        blank=True,
    )
    tech = models.ManyToManyField(
        Tech,
        verbose_name="기술 목록",
        related_name="project_tech",
        null=True,
        blank=True,
    )
    role = models.TextField(
        verbose_name="역할",
        blank=True,
        null=True,
    )
    takeaway = models.TextField(
        verbose_name="배운 점",
        blank=True,
        null=True,
    )
    difficulty = models.TextField(
        verbose_name="어려웠던 점",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "프로젝트"
        db_table = "project"

    def __str__(self):
        return self.title
