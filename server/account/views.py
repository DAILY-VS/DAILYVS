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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')  # 로그인 성공
            else:
                # 로그인 실패
                return redirect('account:login')  
        else:
            return render(request, 'account/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})