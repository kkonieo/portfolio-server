from tabnanny import verbose

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    UserManager,
)
from django.db import models

from apps.core.models import Image, TimeStampModel
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
    is_staff = models.BooleanField(verbose_name="is staff", default=False)

    user_image = models.OneToOneField(
        Image, verbose_name="사용자 이미지", on_delete=models.CASCADE, null=True
    )
    introduction = models.TextField(verbose_name="자기소개", null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name_plural = "사용자"
        db_table = "user"

    def __str__(self):
        return self.email
