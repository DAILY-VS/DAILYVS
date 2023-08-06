from django.shortcuts import redirect
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    # path("mypage/",views.mypage, name='mypage'),
    # path('mypage/update/', views.mypage_update, name='update')
    ]
