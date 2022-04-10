from django.urls import path

from apps.comment.views import CommentListView, CommentView
from apps.project.views import ProjectsView, ProjectView

urlpatterns = [
    path("/<int:project_id>/likes", ProjectView.as_view()),
    path("/<int:project_id>", ProjectView.as_view()),
    path("", ProjectsView.as_view()),  # localhost/projects
    path("/<int:project_id>/comments", CommentListView.as_view()),
    path("/<int:project_id>/comments/<int:comment_id>", CommentView.as_view()),
]
# RESTFUL API
# localhost/projects
