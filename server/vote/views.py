from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from account.models import *
from account.forms import *
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def main(request):
    return render(request, "vote/main.html")


def detail(request):
    return render(request, "vote/detail.html")


def result(request):
    return render(request, "vote/result.html")


# 리스트 페이지
def polls_list(request):
    polls = Poll.objects.all()
    page=request.GET.get('page')
    
    paginator = Paginator(polls,4)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page=1
        page_obj=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        page_obj=paginator.page(page)
    context = {
        'polls': polls,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'vote/list.html', context)

#디테일 페이지
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    poll.increase_views()  # 게시글 조회 수 증가
    print("조회수:", poll.views_count)  # 디버깅용 출력
    
    if not poll.active: #마감이 끝났다면, 투표 불가
        return render(request, 'vote/result.html', {'poll': poll})
    loop_count = poll.choice_set.count() 
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    response =  render(request, 'vote/detail.html', context)
    return response

#좋아요 버튼
@login_required
def poll_like(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        poll_id = req['poll_id']

        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return JsonResponse({'error': '해당 투표가 존재하지 않습니다.'}, status=404)

        if request.user.is_authenticated:
            user = request.user
        else:
            user = AnonymousUser()

        if user.is_authenticated and user.is_active:  # 인증된 사용자 중 활성화된 사용자만 고려
            if poll.poll_like.filter(id=user.id).exists():
                poll.poll_like.remove(user)
                message = "좋아요 취소"
            else:
                poll.poll_like.add(user)
                message = "좋아요"
            
            like_count = poll.poll_like.count()
            context = {'like_count': like_count, 'message': message}
            return JsonResponse(context)
        else:
            return JsonResponse({'error': '로그인이 필요하거나 활성화된 사용자가 아닙니다.'}, status=401)
    else:
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

#마이페이지
def mypage(request):

    polls = Poll.objects.all()
    print(polls)
    context = {
        'polls': polls
    }
    return render(request, 'vote/mypage.html', context)

#마이페이지 수정사항
def mypage_update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('vote:mypage')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'vote/update.html', context)

# 해당 주제 디테일 페이지, PK로 받아오기.
# 반복문 돌리기.
# 결과 페이지
def calcstat(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice') # 뷰에서 선택 불러옴
    print(choice_id)
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = UserVote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        
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

    mbtis = ['ISTJ', 'ISFJ','INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']

    ctx = {
        'total_count':total_count,
        'choice1_count':total_choice1_count,
        'choice2_count':total_choice2_count,
        'man_count':total_man_count,
        'man_choice1_count':total_man_choice1_count,
        'man_choice2_count':total_man_choice2_count,
        'woman_count':total_woman_count,
        'woman_choice1_count':total_woman_choice1_count,
        'woman_choice2_count':total_woman_choice2_count,
        'mbtis':mbtis,
        'mbtis_count':total_mbtis_count,
        'mbtis_choice1_count':total_mbtis_choice1_count,
        'mbtis_choice2_count':total_mbtis_choice2_count,
    }
    
    return render(request, template_name='vote/result.html',context=ctx) 