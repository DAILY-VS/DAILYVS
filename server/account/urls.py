from django.shortcuts import redirect
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'account'

urlpatterns = [
    path('', main, name="main"),
    path('login/', auth_views.LoginView.as_view(template_name='templates/account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'), #회원가입
]