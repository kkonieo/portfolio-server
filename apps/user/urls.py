from django.urls import path

from .views import (
    DecoratedTokenBlacklistView,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DecoratedTokenVerifyView,
    UserListView,
)

urlpatterns = [
    path(
        "login",
        DecoratedTokenObtainPairView.as_view(),
        name="user_token_obtain_pair",
    ),
    path(
        "logout",
        DecoratedTokenBlacklistView.as_view(),
        name="user_logout",
    ),
    path(
        "token/refresh",
        DecoratedTokenRefreshView.as_view(),
        name="user_token_refresh",
    ),
    path(
        "token/verify",
        DecoratedTokenVerifyView.as_view(),
        name="user_token_verify",
    ),
    path(
        "",
        UserListView.as_view(),
        name="user_list",
    ),
]
