from django.contrib import admin

from .models import Position, Tech


@admin.register(Position)
@admin.register(Tech)
class TechAdmin(admin.ModelAdmin):
    # List
    list_display = ("name",)
    # 검색 필터
    search_fields = ("name",)
