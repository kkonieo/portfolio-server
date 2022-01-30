import os
import uuid

from django.db import models
from django.utils import timezone

from apps.core.utility import get_uuid_path


class TimeStampModel(models.Model):
    """
    생성, 수정 날짜 필드를 포함하는 추상 모델
    """

    created_at = models.DateTimeField(
        verbose_name="생성된 날짜", db_index=True, default=timezone.now
    )
    updated_at = models.DateTimeField(verbose_name="수정된 날짜", auto_now=True)

    class Meta:
        abstract = True


class Image(TimeStampModel):

    source = models.ImageField(
        verbose_name="이미지", upload_to=get_uuid_path, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "이미지"
        db_table = "image"

    def __str__(self):
        return self.source.name
