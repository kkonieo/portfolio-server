from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from pyexpat import model

from apps.core.models import DurationModel, Image, TimeStampModel
from apps.core.utility import generate_random_string
from apps.tag.models import Position, Tech
from apps.user.validators import NameValidator


class CustomUserManager(UserManager):
    """
    User Manager
    """

    # 기본 UserManager 는 `username` 필드를 필수로 입력받아 상속받아 재정의 함
    def _create_user(self, name, email, password, **extra_fields):
        """
        이름, 이메일, 패스워드를 입력받고 사용자를 생성합니다.
        """
        if not name:
            raise ValueError("반드시 이름은 설정되어야 합니다.")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        return super().create_user(name, email, password, **extra_fields)

    def create_superuser(self, name, email=None, password=None, **extra_fields):
        return super().create_superuser(name, email, password, **extra_fields)


class User(AbstractBaseUser, TimeStampModel, PermissionsMixin):
    """
    User 모델
    """

    email = models.EmailField(
        primary_key=True,
        unique=True,
        verbose_name="이메일",
        error_messages={
            "unique": "이미 사용중인 이메일 입니다.",
        },
        max_length=60,
    )
    name = models.CharField(
        verbose_name="이름",
        max_length=10,
        validators=[
            NameValidator(),
        ],
    )

    slug = models.CharField(
        verbose_name="프로필 Slug",
        max_length=20,
        unique=True,
        default=generate_random_string,
    )

    is_staff = models.BooleanField(
        verbose_name="is staff",
        default=False,
    )
    user_image = models.OneToOneField(
        Image,
        verbose_name="사용자 이미지",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    introduction = models.TextField(
        verbose_name="자기소개",
        blank=True,
        null=True,
    )
    expected_salary = models.IntegerField(
        verbose_name="희망 연봉",
        blank=True,
        null=True,
    )
    hobby = models.TextField(
        verbose_name="취미",
        blank=True,
        null=True,
    )
    positions = models.ManyToManyField(
        Position,
        verbose_name="포지션",
        related_name="users",
        blank=True,
    )
    tech = models.ManyToManyField(
        Tech,
        verbose_name="기술 목록",
        related_name="users",
        blank=True,
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name_plural = "사용자"
        db_table = "user"

    def __str__(self) -> str:
        return self.email


class Link(TimeStampModel):
    """
    사용자 관련 링크 (블로그, 깃허브 등)
    """

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="link_user",
    )
    source = models.URLField(
        verbose_name="링크 URL",
        max_length=120,
    )

    class Meta:
        verbose_name_plural = "링크"
        db_table = "link"

    def __str__(self) -> str:
        return self.source


class Education(DurationModel, TimeStampModel):
    """
    학력
    """

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="education_user",
    )
    school = models.CharField(
        verbose_name="학교명",
        max_length=50,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name="재학 또는 졸업 상태",
        max_length=10,
        default="졸업",
    )
    department = models.CharField(
        verbose_name="학과",
        max_length=50,
        default="컴퓨터공학과",
    )
    gpa = models.FloatField(
        verbose_name="학점",
        default=3.5,
    )


class Functions(TimeStampModel):
    """
    개발 기능
    """

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="function_user",
    )
    name = models.CharField(
        verbose_name="기능명",
        max_length=50,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="기능 설명",
        blank=True,
        null=True,
    )


class OtherExperience(DurationModel, TimeStampModel):
    """
    교육 및 기타 경험
    """

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="other_experience_user",
    )
    title = models.CharField(
        verbose_name="경험명",
        max_length=50,
        blank=True,
        null=True,
    )
    achievement = models.TextField(
        verbose_name="이수 교과 또는 주요 성취 등",
        blank=True,
        null=True,
    )
    tech = models.ManyToManyField(
        Tech,
        verbose_name="경험에서 사용한 기술 목록",
        related_name="other_experiences",
        blank=True,
        null=True,
    )


class Career(DurationModel, TimeStampModel):
    """
    경력
    """

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="career_user",
    )
    company = models.CharField(
        verbose_name="회사명",
        max_length=50,
        blank=True,
        null=True,
    )
    positions = models.ManyToManyField(
        Position,
        verbose_name="포지션",
        related_name="careers",
        blank=True,
    )
    tech = models.ManyToManyField(
        Tech,
        verbose_name="기술 목록",
        related_name="careers",
        blank=True,
    )
