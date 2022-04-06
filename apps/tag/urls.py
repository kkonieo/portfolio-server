from django.urls import path

from apps.tag.views import PositionView, TechView

urlpatterns = [
    path("tech", TechView.as_view()),
    path("position", PositionView.as_view()),
]
