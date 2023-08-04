from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class TempUser(models.Model): #AbstractUser이용 (id,pw,이름은 O)
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성'),
        ('W', '여성'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
      

class Poll(models.Model): #투표 주제 (게시글)
    owner = models.ForeignKey(TempUser, on_delete=models.CASCADE) #관리자만 등록 가능하면 사용하지 않음
    title = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)#투표올린시간
    active = models.BooleanField(default=True) #마감
    like = models.IntegerField()
    thumbnail = models.ImageField()
    
    def __str__(self):
	    return self.content

class Choice(models.Model): #선택
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    image = models.ImageField()

class UserVote(models.Model): #회원투표
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class NonUserVote(models.Model): #비회원투표
    MBTI = models.TextField()
    GENDERS = (
        ('M', '남성'),
        ('W', '여성'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
