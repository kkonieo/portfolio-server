from django.db import models

# Create your models here.


class Tech(models.Model):
    name = models.CharField(verbose_name="기술", max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "기술"
        db_table = "tech"

    def __str__(self) -> str:
        return self.name


class Position(models.Model):

    name = models.CharField(verbose_name="포지션", max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "포지션"
        db_table = "position"

    def __str__(self) -> str:
        return self.name
