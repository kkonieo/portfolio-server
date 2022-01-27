from django.urls import path

from . import views

urlpatterns = [
    path("/<int:project_id>/likes", views.ProjectsSummaryView.as_view()),
    path("/<int:project_id>", views.ProjectsSummaryView.as_view()),
    path("", views.ProjectsView.as_view()),  # localhost/projects
]
# RESTFUL API
# localhost/projects
