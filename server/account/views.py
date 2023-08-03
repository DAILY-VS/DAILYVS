from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#회원가입
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm 
import requests


User = get_user_model()

def main(request):
    return render(request, "templates/account/login.html")

#회원가입 
def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    return redirect('login:signup')

  else:
    form = SignupForm()
    return render(request, 'templates/account/signup.html', {'form' : form})
  

<<<<<<< HEAD
=======
# Create your views here.


def login(request):
    return render(request, "account/login.html")
>>>>>>> develop
