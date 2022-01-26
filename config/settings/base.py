"""
Django settings for portfolio-server project.

environment variables:
    SECRET_KEY = "secret key"
    ALLOWED_HOSTS = https://aaa.com,https://bbb.com # 접속 허용할 hosts
"""

import os
from datetime import timedelta
from pathlib import Path

env = os.environ

# ------------------------------------------------
# 경로 설정
# ------------------------------------------------

# base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# static directory
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, ".static")

# media
MEDIA_URL = "/media/"  # 웹 URL 을 통해 첨부파일에 점근할 수 있는 URL 경로입니다.
MEDIA_ROOT = os.path.join(BASE_DIR, ".media")  # 실제 파일이 저장될 경로입니다.

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 파일업로드 사이즈의 최대값입니다. 기본값은 2.5MB 입니다.

FIXTURE_DIRS = ["fixtures"]

# 후행 슬래시 비활성화
APPEND_SLASH = False

# ------------------------------------------------
# 보안
# ------------------------------------------------
SECRET_KEY = env.get("SECRET_KEY", "secret key here")
ALLOWED_HOSTS = env.get("ALLOWED_HOSTS", [])

# Debug 기본값 False
DEBUG = False


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------------------------------------------
# 앱
# ------------------------------------------------

# django 앱
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# 써드파티 라이브러리
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # token blacklist
]

# 프로젝트에서 생성한 앱
LOCAL_APPS = [
    "apps.user",
    "apps.core",
    "apps.project",
    "apps.post",
    "apps.comment",
    "apps.skill",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ------------------------------------------------
# 미들웨어
# ------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ------------------------------------------------
# 데이터 베이스
# ------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "user.User"
# ------------------------------------------------
# I18n
# ------------------------------------------------

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

# ------------------------------------------------
# Thrid Party
# ------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

# DRF simplejwt 설정
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),  # access token lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # refresh token lifetime
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "email",  # user PK
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
