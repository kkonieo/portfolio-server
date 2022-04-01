from django.shortcuts import render, redirect, get_object_or_404
from IPython import embed

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm

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


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # embed()
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect('articles:index')
            # next 파라미터 내용이 있으면 next 경로로 보내고, 없으면 메인 페이지로 보낸다.
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    # return render(request, 'accounts/login.html', context)
    # return render(request, 'accounts/auth_form.html', context)
    return render(request, 'accounts/login.html', context)


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