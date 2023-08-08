from django.urls import path, include
from . import views

app_name = "vote"

urlpatterns = [
    
    path("", views.main, name="main"),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/<int:nonuservote_id>', views.poll_nonusergender, name='nonusergender'),
    path('<int:poll_id>/<int:nonuservote_id>/1', views.poll_nonusermbti, name='nonusermbti'),
    path('<int:poll_id>/<int:nonuservote_id>/1/1', views.poll_nonuserfinal, name='nonuserfinal'),
    path('like/', views.poll_like, name='like'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/update/', views.mypage_update, name='update'),
    path("<int:poll_id>/calcstat", views.calcstat, name="calcstat"),
    path("<int:poll_id>/classifyuser", views.classifyuser, name="classifyuser"),
    path('<int:poll_id>/reply/', views.reply, name='reply'),
    path('<int:poll_id>/delete_comment/', views.delete_comment, name='delete_comment'), # 댓글 삭제
    ]
