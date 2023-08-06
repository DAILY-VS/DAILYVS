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


User = get_user_model()

def main(request):
    return render(request, "base.html") ##

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'account/signup.html', {'form': form})
        # 회원가입 실패 시 다시 회원가입 페이지로 리디렉션
    else:
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form})
    
  
def login(request):
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


def logout(request):
    auth.logout(request)

    return redirect("/")


def signup(request):
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
