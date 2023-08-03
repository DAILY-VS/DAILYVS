from django.urls import path, include
from . import views

app_name = "vote"

urlpatterns = [
    
    path("", views.main, name="main"),
    path('list/', views.polls_list, name='list'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),

    
    ]
