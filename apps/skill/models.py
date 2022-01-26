from django.db import models

# Create your models here.


class Skill(models.Model):
    name = models.CharField(verbose_name="기술", max_length=40, unique=True)

    class Meta:
        verbose_name_plural = "기술"
        db_table = "skill"

    def __str__(self) -> str:
        return self.name
