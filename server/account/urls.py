from django.shortcuts import redirect
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'account'

urlpatterns = [
    #path('', main, name="main"),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
]
