from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    # path("mypage/",views.mypage, name='mypage'),
    # path('mypage/update/', views.mypage_update, name='update')
    ]
