from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Link, User


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("정보"), {"fields": ("source", "user")}),
        (
            _("Date/time"),
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")
    list_display = ("source", "user", "created_at")
    search_fields = ("source", "user")
    ordering = ("source", "user")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Edit
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "email",
                    "slug",
                    "password",
                    "user_image",
                    "introduction",
                    "skills",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Date/time"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # manytomany field 추가 삭제
    filter_horizontal = ("skills",)
    # 읽기 전용 필드
    readonly_fields = ("created_at", "updated_at")
    # List
    list_display = ("email", "name", "is_staff", "last_login")
    # 리스트 필터
    list_filter = ("is_staff", "is_superuser", "groups", "created_at", "last_login")
    # 검색 필터
    search_fields = ("name", "email")
    ordering = ("email",)
