from django.urls import include, path

from .views import (
    DecoratedTokenBlacklistView,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DecoratedTokenVerifyView,
    DeveloperListView,
    UserListView,
    UserRegisterView,
    UserView,
)

single_user_urls = [
    path(
        "register",
        UserRegisterView.as_view(),
        name="user_register",
    ),
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
]

user_list_urls = [
    path(
        "",
        UserListView.as_view(),
        name="user_list",
    ),
    path(
        "developers",
        DeveloperListView.as_view(),
        name="developer_list",
    ),
    path(
        "<str:slug>",
        UserView.as_view(),
        name="user",
    ),
]

urlpatterns = [
    path("user/", include(single_user_urls)),
    path("users/", include(user_list_urls)),
]
