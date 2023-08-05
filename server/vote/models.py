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
    poll_like = models.ManyToManyField('account.User', blank=True, related_name='likes')
    views_count = models.PositiveIntegerField(default=0)  # 조회 숫자 필드
    
    def increase_views(self):
        self.views_count=self.views_count+1
        self.save()

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
    
    # def choice_get_vote_count(self):
    #     User.objects.filter('mbti'=='infj')
    #     return self.vote_set.count()
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

class NonUserVote(models.Model):
    mbti=models.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
 
 #  def calcstat(request):
#     votes = Vote.objects.filter(choice__poll__pk=1)
#     result = votes.values("user__gender", "user__mbti", "choice_id").annotate(total=Count("*"))
        
#     user_total_count = votes.count()
#     print(user_total_count)

#     result_gender = votes.values("user__gender", "choice_id").annotate(total=Count("*"))
#     gender_w = [group for group in result_gender if group["user__gender"] == "W"]
#     print(gender_w)