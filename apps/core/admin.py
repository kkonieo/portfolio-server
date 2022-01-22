from django.contrib import admin

from apps.core.models import Image

# Register your models here.


@admin.register(Image)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
    )
