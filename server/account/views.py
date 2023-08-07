from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from vote.models import *


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