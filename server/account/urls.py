from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    path("/login", views.login, name="login"),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('signup/', signup, name='signup'), #회원가입
]