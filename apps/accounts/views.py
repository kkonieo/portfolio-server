from django.shortcuts import render, redirect, get_object_or_404
from IPython import embed

import requests
from rest_framework import status
from django.http import JsonResponse
from json.decoder import JSONDecodeError

from apps.accounts.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm

from django.conf import settings

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view


BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'

state = getattr(settings, 'STATE')

# Create your views here.

#Authentication(인증) -> 신원확인
#  - 자신이 누구라고 주장하는 사람의 신원을 확인하는 것

# Auth CRUD : CREATE
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        # embed()
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm
    context = {'form':form}
    # return render(request, 'accounts/signup.html', context)
    return render(request, 'accounts/auth_form.html', context)


# def login(request):
#     if request.user.is_authenticated:
#         return redirect('articles:index')

#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         # embed()
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             # return redirect('articles:index')
#             # next 파라미터 내용이 있으면 next 경로로 보내고, 없으면 메인 페이지로 보낸다.
#             return redirect(request.GET.get('next') or 'articles:index')
#     else:
#         form = AuthenticationForm()
#     context = {'form':form}
#     # return render(request, 'accounts/login.html', context)
#     # return render(request, 'accounts/auth_form.html', context)
#     return render(request, 'accounts/login.html', context)

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )
def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)
    email = kakao_account.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


# 회원탈퇴 - 로그인한 사람만 보임
@require_POST
def delete(request):
    request.user.delete()
    return redirect('articles:index')


# 회원정보 수정 
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        # form = UserChangeForm(instance=request.user)
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    # return render(request,'accounts/update.html', context)
    return render(request,'accounts/auth_form.html', context)


# 비밀번호 변경 
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    # return render(request,'accounts/change_password.html', context)
    return render(request,'accounts/auth_form.html', context)


# Profile 
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {'person':person}
    return render(request,'accounts/profile.html', context)