from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from account.models import *
from account.forms import *
from datetime import datetime, timedelta
# Create your views here.


def main(request):
    return render(request, "vote/main.html")


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

# 리스트 페이지
def polls_list(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'vote/list.html', context)

#디테일 페이지
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active: #마감이 끝났다면
        return render(request, 'vote/result.html', {'poll': poll})
    loop_count = poll.choice_set.count() 
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    response =  render(request, 'vote/detail.html', context)
    
   #조회수 기능 (쿠키 이용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('view', '_')

    if f'_{poll_id}_' not in cookie_value:
        cookie_value += f'{poll_id}_'
        response.set_cookie('view', value=cookie_value, max_age=max_age, httponly=True)
        poll.views_count += 1
        poll.save()
    return response

    



# 결과 페이지
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice') # 뷰에서 선택 불러옴
        
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'vote/result.html', {'poll': poll})
    


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


def mypage(request):

    polls = Poll.objects.all()
    print(polls)
    context = {
        'polls': polls
    }
    return render(request, 'vote/mypage.html', context)


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