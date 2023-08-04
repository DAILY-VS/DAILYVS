from django.urls import path, include
from . import views

app_name = "vote"

urlpatterns = [
    path("", views.main, name="main"),
    path("calcstat", views.calcstat, name="calcstat"),
    path("detail/", views.detail, name="detail"),
    path("result/", views.result, name="result"),
]
