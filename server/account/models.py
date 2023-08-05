from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager


#컨텐츠에 따라서
# JOBS = (
#     ('P', '교수/강사(Professor/Lecturer)'),
#     ('S', '학생(Student)'),
#     ('R', '연구원(Researcher)'),
#     ('E', '기타(Etc.)')
# )
# job = models.CharField(verbose_name='직업', max_length=1, choices=JOBS)

#회원일 때
class User(AbstractUser): #AbstractUser이용 (id,pw,이름은 O)
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)


#비회원일 때
class NonUser(models.Model):
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)

