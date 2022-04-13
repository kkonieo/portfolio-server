from django.urls import path

from apps.comment.views import CommentListView, CommentView
from apps.project.views import LikeListView, LikeView, ProjectListView, ProjectView

urlpatterns = [
    path("", ProjectListView.as_view()),
    path("/<int:project_id>", ProjectView.as_view()),
    path("/<int:project_id>/comments", CommentListView.as_view()),
    path("/<int:project_id>/comments/<int:comment_id>", CommentView.as_view()),
    path("/<int:project_id>/likes", LikeListView.as_view()),
    path("/<int:project_id>/like", LikeView.as_view()),
]
