from django.urls import path

from apps.core.views import ImageView

urlpatterns = [
    path("image", ImageView.as_view()),
]
