from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser): #user 정보
    GENDERS = (
    ('M', '남성(Man)'),
    ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
    nickname = models.CharField(verbose_name='닉네임',max_length=20)
    mbti=models.CharField(max_length=4)
    
    
    def __str__(self):
        return self.username