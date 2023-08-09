from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from account.models import User

# Create your models here.
class Poll(models.Model): #이미지, 제목, 좋아요 추가
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    title = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    poll_like = models.ManyToManyField('account.User', blank=True, related_name='likes')
    views_count = models.PositiveIntegerField(default=0)  # 조회 숫자 필드
    thumbnail = models.ImageField()
    # created_at = models.DateTimeField(auto_now_add=True)    

    def increase_views(self):
        self.views_count=self.views_count+1
        self.save()

    def __str__(self):
        return self.title

class Choice(models.Model): #이미지 추가
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    image = models.ImageField()
class UserVote(models.Model): #회원투표
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class NonUserVote(models.Model): #비회원투표
    MBTI = models.TextField(null= True)
    GENDERS = (
        ('M', '남성'),
        ('W', '여성'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, null= True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    
class Comment(models.Model): #댓글
    user_info = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
   
    def __str__(self):
        return self.content