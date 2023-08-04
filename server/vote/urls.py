from django.urls import path, include
from . import views

app_name = "vote"

urlpatterns = [
<<<<<<< HEAD
    
    path("", views.main, name="main"),
    path('list/', views.polls_list, name='list'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),

    
    ]
=======
    path("", views.main, name="main"),
    path("calcstat", views.calcstat, name="calcstat"),
]
>>>>>>> 9a582c9e1128f8d07e4d79aa1a98a5100133c0dd
