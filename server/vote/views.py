from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages


# Create your views here.


def main(request):
    return render(request, "vote/main.html")

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
    return render(request, 'vote/detail.html', context)

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