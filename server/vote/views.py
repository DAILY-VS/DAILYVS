from django.shortcuts import render
<<<<<<< HEAD
from django.db.models import Count
from django.http import HttpResponse
from vote.models import *
=======
from django.http import JsonResponse
import json

# Create your views here.
>>>>>>> develop


def main(request):
    
    return render(request, "vote/main.html")

<<<<<<< HEAD
# 해당 주제 디테일 페이지, PK로 받아오기.
# 반복문 돌리기.



def calcstat(request):
    mbtis = ['ISTJ', 'ISFJ','INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']

    print('User')
    user_poll = UserVote.objects.filter(choice__poll__pk=1)
    user_total_count=user_poll.count()
    print('user_total_count : ' + str(user_total_count))

    user_choice1 = user_poll.filter(choice_id=1)
    user_choice1_count=user_choice1.count()
    print('user_choice1_count : ' + str(user_choice1_count))

    user_choice2 = user_poll.filter(choice_id=2)
    user_choice2_count=user_choice2.count()
    print('user_choice2_count : ' + str(user_choice2_count))   

    user_man = UserVote.objects.filter(choice__poll__pk=1, user__gender='M')
    user_man_count=user_man.count()
    print('user_man_count : ' + str(user_man_count))

    user_man_choice1 = user_man.filter(choice_id=1)
    user_man_choice1_count=user_man_choice1.count()
    print('user_man_choice1_count : ' + str(user_man_choice1_count))

    user_man_choice2 = user_man.filter(choice_id=2)
    user_man_choice2_count=user_man_choice2.count()
    print('user_man_choice2_count : ' + str(user_man_choice2_count))

    user_woman = UserVote.objects.filter(choice__poll__pk=1, user__gender='W')
    user_woman_count= user_woman.count()
    print('user_woman_count : ' + str(user_woman_count))

    user_woman_choice1 = user_woman.filter(choice_id=1)
    user_woman_choice1_count=user_woman_choice1.count()
    print('user_woman_choice1_count : ' + str(user_woman_choice1_count))

    user_woman_choice2 = user_woman.filter(choice_id=2)
    user_woman_choice2_count=user_woman_choice2.count()
    print('user_woman_choice2_count : ' + str(user_woman_choice2_count))

    user_mbtis_count=[]
    user_mbtis_choice1_count=[]
    user_mbtis_choice2_count=[]

    for mbti in mbtis : 
        user_mbti = UserVote.objects.filter(choice__poll__pk=1, user__mbti= mbti)
        user_mbti_count=user_mbti.count()  
        user_mbtis_count.append(user_mbti_count) 

        user_mbti_choice1 = user_mbti.filter(choice_id=1)
        user_mbti_choice1_count= user_mbti_choice1.count()
        user_mbtis_choice1_count.append(user_mbti_choice1_count)

        user_mbti_choice2 = user_mbti.filter(choice_id=2)
        user_mbti_choice2_count= user_mbti_choice2.count()
        user_mbtis_choice2_count.append(user_mbti_choice2_count)

    print('user_mbtis_count : ' + str(user_mbtis_count))
    print('user_mbtis_choice1_count : ' + str(user_mbtis_choice1_count))
    print('user_mbtis_choice2_count : ' + str(user_mbtis_choice2_count))

    print('\nNonUser')
    nonuser_poll=NonUserVote.objects.filter(choice__poll__pk=1)
    nonuser_total_count=nonuser_poll.count()
    print('nonuser_total_count : ' + str(nonuser_total_count))

    nonuser_choice1 = nonuser_poll.filter(choice_id=1)
    nonuser_choice1_count=nonuser_choice1.count()
    print('nonuser_choice1_count : ' + str(nonuser_choice1_count))

    nonuser_choice2 = nonuser_poll.filter(choice_id=2)
    nonuser_choice2_count=nonuser_choice2.count()
    print('nonuser_choice2_count : ' + str(nonuser_choice2_count))   

    nonuser_man = NonUserVote.objects.filter(choice__poll__pk=1, gender='M')
    nonuser_man_count=nonuser_man.count()
    print('nonuser_man_count : ' + str(nonuser_man_count))
    
    nonuser_man_choice1 = nonuser_man.filter(choice_id=1)
    nonuser_man_choice1_count=nonuser_man_choice1.count()
    print('nonuser_man_choice1_count : ' + str(nonuser_man_choice1_count))

    nonuser_man_choice2 = nonuser_man.filter(choice_id=2)
    nonuser_man_choice2_count=nonuser_man_choice2.count()
    print('nonuser_man_choice2_count : ' + str(nonuser_man_choice2_count))

    nonuser_woman = NonUserVote.objects.filter(choice__poll__pk=1, gender='W')
    nonuser_woman_count=nonuser_woman.count()
    print('nonuser_woman_count : ' + str(nonuser_woman_count))

    nonuser_woman_choice1 = nonuser_woman.filter(choice_id=1)
    nonuser_woman_choice1_count=nonuser_woman_choice1.count()
    print('nonuser_woman_choice1_count : ' + str(nonuser_woman_choice1_count))

    nonuser_woman_choice2 = nonuser_woman.filter(choice_id=2)
    nonuser_woman_choice2_count=nonuser_woman_choice2.count()
    print('nonuser_woman_choice2_count : ' + str(nonuser_woman_choice2_count))

    nonuser_mbtis_count=[]
    nonuser_mbtis_choice1_count=[]
    nonuser_mbtis_choice2_count=[]

    for mbti in mbtis : 
        nonuser_mbti = NonUserVote.objects.filter(choice__poll__pk=1, MBTI = mbti)
        nonuser_mbti_count=nonuser_mbti.count()  
        nonuser_mbtis_count.append(nonuser_mbti_count) 

        nonuser_mbti_choice1 = nonuser_mbti.filter(choice_id=1)
        nonuser_mbti_choice1_count= nonuser_mbti_choice1.count()
        nonuser_mbtis_choice1_count.append(nonuser_mbti_choice1_count)

        nonuser_mbti_choice2 = nonuser_mbti.filter(choice_id=2)
        nonuser_mbti_choice2_count= nonuser_mbti_choice2.count()
        nonuser_mbtis_choice2_count.append(nonuser_mbti_choice2_count)

    print('nonuser_mbtis_count : ' + str(nonuser_mbtis_count))
    print('nonuser_mbtis_choice1_count : ' + str(nonuser_mbtis_choice1_count))
    print('nonuser_mbtis_choice2_count : ' + str(nonuser_mbtis_choice2_count))

    print('\nTotal')
    total_count = user_total_count + nonuser_total_count

    print('total_count : ' + str(total_count))
    total_choice1_count = user_choice1_count + nonuser_choice1_count

    print('total_choice1_count : ' + str(total_choice1_count))
    total_choice2_count = user_choice2_count + nonuser_choice2_count
    print('total_choice2_count : ' + str(total_choice2_count))
    total_man_count = user_man_count + nonuser_man_count

    print('total_man_count : ' + str(total_man_count))
    total_man_choice1_count = user_man_choice1_count + nonuser_man_choice1_count
    print('total_man_choice1_count : ' + str(total_man_choice1_count))
    total_man_choice2_count = user_man_choice2_count + nonuser_man_choice2_count
    print('total_man_choice2_count : ' + str(total_man_choice2_count))   

    total_woman_count = user_woman_count + nonuser_woman_count
    print('total_woman_count : ' + str(total_woman_count))
    total_woman_choice1_count = user_woman_choice1_count + nonuser_woman_choice1_count
    print('total_woman_choice1_count : ' + str(total_woman_choice1_count))
    total_woman_choice2_count = user_woman_choice2_count + nonuser_woman_choice2_count
    print('total_woman_choice2_count : ' + str(total_woman_choice2_count))   

    total_mbtis_count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    total_mbtis_choice1_count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    total_mbtis_choice2_count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range (16):
        total_mbtis_count[i] = user_mbtis_count[i] + nonuser_mbtis_count[i]
        total_mbtis_choice1_count[i] = user_mbtis_choice1_count[i] + nonuser_mbtis_choice1_count[i]
        total_mbtis_choice2_count[i] = user_mbtis_choice2_count[i] + nonuser_mbtis_choice2_count[i]

    print('total_mbtis_count : ' + str(total_mbtis_count))   
    print('total_mbtis_choice1_count : ' + str(total_mbtis_choice1_count))   
    print('total_mbtis_choice2_count : ' + str(total_mbtis_choice2_count))   

    return render(request, template_name='vote/base.html')
=======

def detail(request):
    return render(request, "vote/detail.html")


def result(request):
    return render(request, "vote/result.html")


def result_view(request):
    approval_percentage = 75
    disapproval_percentage = 25

    return render(
        request,
        "result.html",
        {
            "approval_percentage": approval_percentage,
            "disapproval_percentage": disapproval_percentage,
        },
    )
>>>>>>> develop
