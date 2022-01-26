from django.urls import path

from . import views

urlpatterns = [
    path("project-card/", views.ProjectCardList.as_view()),
    path("project-summary/", views.ProjectSummaryList.as_view()),
    path("project/", views.ProjectList.as_view()),
]
