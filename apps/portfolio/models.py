from django.conf import settings
from django.db import models

from apps.core.models import TimeStampModel


class Portfolio(TimeStampModel):
    """
    Portfolio 모델
    """

    title = models.CharField(verbose_name="포트폴리오 제목", max_length=40)
    content = models.TextField(verbose_name="포트폴리오 내용")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="사용자", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
