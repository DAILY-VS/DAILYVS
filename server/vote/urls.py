from django.urls import path, include
from . import views

app_name = "vote"

urlpatterns = [path("", views.main, name="main")]
