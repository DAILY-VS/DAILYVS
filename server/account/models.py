from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, UserManager



#비회원일 때
class NonUser(models.Model):
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)

# Create your models here.
class User(AbstractUser): #AbstractUser이용 (id,pw,이름은 O)
    GENDERS = (
    ('M', '남성(Man)'),
    ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
    nickname = models.CharField(max_length=20)
    mbti=models.CharField(max_length=4)
    
    
    def __str__(self):
        return self.username
