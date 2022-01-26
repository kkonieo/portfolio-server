from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # List
    list_display = ("name",)
    # 검색 필터
    search_fields = ("name",)
