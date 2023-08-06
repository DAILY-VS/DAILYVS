from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from vote.models import *
#비밀번호 변경
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
#회원 탈퇴
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import User


def signup(request): # 회원가입
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('vote:list')
        else:
            ctx={
                'form':form,
            }
            return render(request, 'account/signup.html',context=ctx)
    else:
        form = SignupForm()
        ctx = {
            'form': form,
        }
        return render(request, template_name='account/signup.html', context=ctx)

def login(request): #로그인
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('vote:list')
        else:
            context = {
                'form': form,
            }
            return render(request, 'account/login.html', context=context)
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context=context)

def logout(request): #로그아웃
    auth.logout(request)
    return redirect("/")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 변경 후 로그인 상태 유지
            return redirect('vote:mypage')  # 변경 후 이동할 페이지
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'account/change_password.html', context)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'account/delete.html'
    success_url = reverse_lazy('/') 
    form_class = UserDeleteForm

    def get_object(self, queryset=None):
        return self.request.user