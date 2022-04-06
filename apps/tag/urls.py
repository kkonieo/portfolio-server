from django.urls import path

from apps.tag.views import TechView

urlpatterns = [
    path("tech", TechView.as_view()),
]
