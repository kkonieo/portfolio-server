from django.urls import path

from . import views

urlpatterns = [
    path("image", views.ImageView.as_view()),
]
