from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, UserManager


# 비회원일 때
class NonUser(models.Model):
    mbti = models.CharField(max_length=4)
    GENDERS = (
        ("M", "남성(Man)"),
        ("W", "여성(Woman)"),
    )
    gender = models.CharField(verbose_name="성별", max_length=1, choices=GENDERS)


# Create your models here.
class User(AbstractUser):  # user 정보
    GENDERS = (
        ("M", "남성(Man)"),
        ("W", "여성(Woman)"),
    )
    gender = models.CharField(verbose_name="성별", max_length=1, choices=GENDERS)
    nickname = models.CharField(max_length=20)
    MBTI_set = (
        ("INFP", "INFP"),
        ("ENFP", "ENFP"),
        ("INFJ", "INFJ"),
        ("ENFJ", "ENFJ"),
        ("INTJ", "INTJ"),
        ("ENTJ", "ENTJ"),
        ("INTP", "INTP"),
        ("ENTP", "ENTP"),
        ("ISFP", "ISFP"),
        ("ESFP", "ESFP"),
        ("ISFJ", "ISFJ"),
        ("ESFJ", "ESFJ"),
        ("ISTP", "ISTP"),
        ("ESTP", "ESTP"),
        ("ISTJ", "ISTJ"),
        ("ESTJ", "ESTJ"),
    )
    mbti=models.CharField(verbose_name='MBTI', max_length=4, choices=MBTI_set)
    nickname = models.CharField(verbose_name='닉네임',max_length=20)
    voted_polls = models.ManyToManyField('vote.Poll', blank=True, related_name='voters')

    def __str__(self):
        return self.username
