from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    # url 패던에서 str을 사용하면 맨아래에 위치해서 마지막에 탐색되게 해야한다. 조건을 붙일경우에는 위치상관없음
    path('<str:username>/', views.profile, name='profile'),

    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),

]