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
    # birth_date = models.DateField(verbose_name='생년월일')

#비회원일 때
class NonUser(models.Model):
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)



##################################################################################

class Poll(models.Model): #투표 주제 (게시글)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #관리자만 등록 가능하면 사용하지 않음
	title = models.TextField()
	content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)#투표올린시간
    active = models.BooleanField(default=True) #마감

    def __str__(self):
	        return self.text

class Choice(models.Model): #선택
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

class UserVote(models.Model): #회원투표
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class NonUserVote(models.Model): #비회원투표
    # NonUser = models.ForeignKey(NonUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class Comment():
    # 부모식별자
	content=models.CharField(max_length=255)
    info = models.ForeignKey(UserVote, on_delete=models.CASCADE)

class Statistics():
	uservote = models.ForeignKey(UserVote, on_delete=models.CASCADE)
	nonuservote = models.ForeignKey(NonUserVote, on_delete=models.CASCADE)