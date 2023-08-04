from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
<<<<<<< HEAD
    
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    
    ]
=======
    path("/login", views.login, name="login")
]
>>>>>>> 9a582c9e1128f8d07e4d79aa1a98a5100133c0dd
