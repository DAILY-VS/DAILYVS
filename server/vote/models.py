from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from account.models import *

# Create your models here.
class Poll(models.Model): #이미지, 제목, 좋아요 추가
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.text
    
    def user_can_vote(self, user): #이미 투표한 유저 못하도록
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True
    
    @property
    def get_vote_count(self): #총 투표수
        return self.vote_set.count() #객체에 접근할 수 있는 이름은 모델명(소문자)_set
    
    def get_result_dict(self):
        res = [] # 리스트를 만들기 위함
        for choice in self.choice_set.all():
            d = {} #디렉토리 만들기 위함
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100 # 선택한 투표 수/총 투표 수
            res.append(d) #리스트 안에 디렉토리 구조
        return res
    
class Choice(models.Model): #이미지 추가
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

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
