from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse
from vote.models import *


def main(request):
    return render(request, "vote/main.html")

# 해당 주제 디테일 페이지, PK로 받아오기.
# 반복문 돌리기.

def calcstat(request):
    poll = UserVote.objects.filter(choice__poll__pk=1)
    total_count=poll.count()
    print(total_count)

    choice1 = poll.filter(choice=1)
    choice1_count=choice1.count()
    print(choice1_count)

    choice2 = poll.filter(choice=2)
    choice2_count=choice2.count()
    print(choice2_count)    

    man = UserVote.objects.filter(choice__poll__pk=1, user__gender='M')
    man_count=man.count()
    print(man_count)

    woman = UserVote.objects.filter(choice__poll__pk=1, user__gender='W')
    woman_count= woman.count()
    print(woman_count)

    mbtis = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']
    mbtis_count=[]

    for mbti in mbtis : 
        a = UserVote.objects.filter(choice__poll__pk=1, user__mbti= mbti)
        a_count=a.count()  
        mbtis_count.append(a_count) 

    print(mbtis_count)
    return render(request, template_name='vote/base.html')