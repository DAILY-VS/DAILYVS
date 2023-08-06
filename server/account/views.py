from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#회원가입
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm 
import requests
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
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
from .forms import UserChangeForm, UserDeleteForm

User = get_user_model()

def main(request):
    return render(request, "base.html") ##

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

  
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('/')
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


def logout(request):
    auth.logout(request)

    return redirect("/")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            return redirect('/')
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


def mypage(request):

    polls = Poll.objects.all()
    print(polls)
    context = {
        'polls': polls
    }
    return render(request, 'vote/mypage.html', context)

def mypage_update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:mypage')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'account/update.html', context)



class UserDeleteView(DeleteView):
    model = User
    template_name = 'account/delete.html'
    success_url = reverse_lazy('vote:mypage') 
    form_class = UserDeleteForm

    def get_object(self, queryset=None):
        return self.request.user