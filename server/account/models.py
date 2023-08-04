from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser): #AbstractUser이용 (id,pw,이름은 O)
    GENDERS = (
    ('M', '남성(Man)'),
    ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
    mbti=models.CharField(max_length=4)
    
    def __str__(self):
        return self.username



