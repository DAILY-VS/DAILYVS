import json
from .models import *
from account.forms import *
from account.models import *
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#메인페이지
def main(request):
    polls = Poll.objects.all()
    sort = request.GET.get("sort")

    if sort == "popular":
        polls = polls.order_by("-views_count")  # 인기순
    elif sort == "latest":
        polls = polls.order_by("-id")  # 최신순
    elif sort == "oldest":
        polls = polls.order_by("id")  # 등록순

    page = request.GET.get("page")

    paginator = Paginator(polls, 4)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    context = {
        "polls": polls,
        "page_obj": page_obj,
        "paginator": paginator,
    }

    return render(request, "vote/main.html", context)

# 투표 디테일 페이지
def poll_detail(request, poll_id):
    user = request.user 
    poll = get_object_or_404(Poll, id=poll_id)

    if user.is_authenticated and user.voted_polls.filter(id=poll_id).exists():
        calcstat_url = reverse("vote:calcstat", args=[poll_id])
        return redirect(calcstat_url)
    else:
        poll.increase_views()  # 게시글 조회 수 증가
        loop_count = poll.choice_set.count()
        context = {
            "poll": poll,
            "loop_time": range(0, loop_count),
        }
        response = render(request, "vote/detail.html", context)
        return response

#투표 게시글 좋아요 
@login_required
def poll_like(request):
    if request.method == "POST":
        req = json.loads(request.body)
        poll_id = req["poll_id"]
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return JsonResponse({"error": "해당 투표가 존재하지 않습니다."}, status=404)

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
            context = {"like_count": like_count, "message": message}
            return JsonResponse(context)
        else:
            return JsonResponse({"error": "로그인이 필요하거나 활성화된 사용자가 아닙니다."}, status=401)
    else:
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

#유저 마이페이지
@login_required(login_url='/account/login/') # 비로그인시 /mypage 막음
def mypage(request):
    polls = Poll.objects.all()
    page = request.GET.get("page")
    paginator = Paginator(polls, 4)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    context = {
        "polls": polls,
        "page_obj": page_obj,
        "paginator": paginator,
    }
    return render(request, "vote/mypage.html", context)

#마이페이지 정보 수정
@login_required(login_url='/account/login/') # 비로그인시 mypage/update 막음
def mypage_update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("vote:mypage")
    else:
        form = UserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "vote/update.html", context)

#댓글

#투표 시 회원, 비회원 구분 
def classifyuser(request, poll_id):
    if request.method == "POST" : 
        poll = get_object_or_404(Poll, pk=poll_id)
        choice_id = request.POST.get("choice")  # 뷰에서 선택 불러옴
        user = request.user
        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            try : 
                vote = UserVote(user=request.user, poll=poll, choice=choice)
                vote.save()
                user.voted_polls.add(poll_id)
                calcstat_url = reverse("vote:calcstat", args=[poll_id])
                return redirect(calcstat_url)
            except ValueError: 
                vote = NonUserVote(poll=poll, choice=choice)
                vote.save()
                nonuservote_id = vote.id 
                poll = get_object_or_404(Poll, pk=poll_id)
                context = {
                    "poll": poll,
                    "gender": ["M", "W"],
                    "nonuservote_id": nonuservote_id,
                    "loop_time": range(0, 2),
                }
                return render(request, "vote/detail2.html", context)

#회원/비회원 투표 통계 계산 및 결과 페이지
def calcstat(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    mbtis = [
        "ISTJ",
        "ISFJ",
        "INFJ",
        "INTJ",
        "ISTP",
        "ISFP",
        "INFP",
        "INTP",
        "ESTP",
        "ESFP",
        "ENFP",
        "ENTP",
        "ESTJ",
        "ESFJ",
        "ENFJ",
        "ENTJ",
    ]

    user_poll = UserVote.objects.filter(choice__poll__pk=poll_id)
    user_total_count = user_poll.count()

    user_choice1 = user_poll.filter(choice_id=2*poll_id-1)
    user_choice1_count = user_choice1.count()

    user_choice2 = user_poll.filter(choice_id=2*poll_id)
    user_choice2_count = user_choice2.count()

    user_man = UserVote.objects.filter(choice__poll__pk=poll_id, user__gender="M")
    user_man_count = user_man.count()

    user_man_choice1 = user_man.filter(choice_id=2*poll_id-1)
    user_man_choice1_count = user_man_choice1.count()

    user_man_choice2 = user_man.filter(choice_id=2*poll_id)
    user_man_choice2_count = user_man_choice2.count()

    user_woman = UserVote.objects.filter(choice__poll__pk=poll_id, user__gender="W")
    user_woman_count = user_woman.count()

    user_woman_choice1 = user_woman.filter(choice_id=2*poll_id-1)
    user_woman_choice1_count = user_woman_choice1.count()

    user_woman_choice2 = user_woman.filter(choice_id=2*poll_id)
    user_woman_choice2_count = user_woman_choice2.count()

    user_mbtis_count = []
    user_mbtis_choice1_count = []
    user_mbtis_choice2_count = []

    for mbti in mbtis:
        user_mbti = UserVote.objects.filter(choice__poll__pk=poll_id, user__mbti=mbti)
        user_mbti_count = user_mbti.count()
        user_mbtis_count.append(user_mbti_count)

        user_mbti_choice1 = user_mbti.filter(choice_id=2*poll_id-1)
        user_mbti_choice1_count = user_mbti_choice1.count()
        user_mbtis_choice1_count.append(user_mbti_choice1_count)

        user_mbti_choice2 = user_mbti.filter(choice_id=2*poll_id)
        user_mbti_choice2_count = user_mbti_choice2.count()
        user_mbtis_choice2_count.append(user_mbti_choice2_count)

    nonuser_poll = NonUserVote.objects.filter(choice__poll__pk=poll_id)
    nonuser_total_count = nonuser_poll.count()

    nonuser_choice1 = nonuser_poll.filter(choice_id=2*poll_id-1)
    nonuser_choice1_count = nonuser_choice1.count()

    nonuser_choice2 = nonuser_poll.filter(choice_id=2*poll_id)
    nonuser_choice2_count = nonuser_choice2.count()

    nonuser_man = NonUserVote.objects.filter(choice__poll__pk=poll_id, gender="M")
    nonuser_man_count = nonuser_man.count()

    nonuser_man_choice1 = nonuser_man.filter(choice_id=2*poll_id-1)
    nonuser_man_choice1_count = nonuser_man_choice1.count()

    nonuser_man_choice2 = nonuser_man.filter(choice_id=2*poll_id)
    nonuser_man_choice2_count = nonuser_man_choice2.count()

    nonuser_woman = NonUserVote.objects.filter(choice__poll__pk=poll_id, gender="W")
    nonuser_woman_count = nonuser_woman.count()

    nonuser_woman_choice1 = nonuser_woman.filter(choice_id=2*poll_id-1)
    nonuser_woman_choice1_count = nonuser_woman_choice1.count()

    nonuser_woman_choice2 = nonuser_woman.filter(choice_id=2*poll_id)
    nonuser_woman_choice2_count = nonuser_woman_choice2.count()

    nonuser_mbtis_count = []
    nonuser_mbtis_choice1_count = []
    nonuser_mbtis_choice2_count = []

    for mbti in mbtis:
        nonuser_mbti = NonUserVote.objects.filter(choice__poll__pk=poll_id, MBTI=mbti)
        nonuser_mbti_count = nonuser_mbti.count()
        nonuser_mbtis_count.append(nonuser_mbti_count)

        nonuser_mbti_choice1 = nonuser_mbti.filter(choice_id=2*poll_id-1)
        nonuser_mbti_choice1_count = nonuser_mbti_choice1.count()
        nonuser_mbtis_choice1_count.append(nonuser_mbti_choice1_count)

        nonuser_mbti_choice2 = nonuser_mbti.filter(choice_id=2*poll_id)
        nonuser_mbti_choice2_count = nonuser_mbti_choice2.count()
        nonuser_mbtis_choice2_count.append(nonuser_mbti_choice2_count)

    total_count = user_total_count + nonuser_total_count

    total_choice1_count = user_choice1_count + nonuser_choice1_count

    total_choice2_count = user_choice2_count + nonuser_choice2_count
    total_man_count = user_man_count + nonuser_man_count

    total_man_choice1_count = user_man_choice1_count + nonuser_man_choice1_count
    total_man_choice2_count = user_man_choice2_count + nonuser_man_choice2_count

    total_woman_count = user_woman_count + nonuser_woman_count
    total_woman_choice1_count = user_woman_choice1_count + nonuser_woman_choice1_count
    total_woman_choice2_count = user_woman_choice2_count + nonuser_woman_choice2_count

    total_mbtis_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_mbtis_choice1_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_mbtis_choice2_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(16):
        total_mbtis_count[i] = user_mbtis_count[i] + nonuser_mbtis_count[i]
        total_mbtis_choice1_count[i] = (
            user_mbtis_choice1_count[i] + nonuser_mbtis_choice1_count[i]
        )
        total_mbtis_choice2_count[i] = (
            user_mbtis_choice2_count[i] + nonuser_mbtis_choice2_count[i]
        )

    mbtis = [
        "ISTJ",
        "ISFJ",
        "INFJ",
        "INTJ",
        "ISTP",
        "ISFP",
        "INFP",
        "INTP",
        "ESTP",
        "ESFP",
        "ENFP",
        "ENTP",
        "ESTJ",
        "ESFJ",
        "ENFJ",
        "ENTJ",
    ]
    choice1_percentage = int(total_choice1_count / total_count * 100)
    choice2_percentage = int(total_choice2_count / total_count * 100)

    ctx = {
        "total_count": total_count,
        "choice1_count": total_choice1_count,
        "choice2_count": total_choice2_count,
        "choice1_percentage": choice1_percentage,
        "choice2_percentage": choice2_percentage,
        "man_count": total_man_count,
        "man_choice1_count": total_man_choice1_count,
        "man_choice2_count": total_man_choice2_count,
        "woman_count": total_woman_count,
        "woman_choice1_count": total_woman_choice1_count,
        "woman_choice2_count": total_woman_choice2_count,
        "mbtis": mbtis,
        "mbtis_count": total_mbtis_count,
        "mbtis_choice1_count": total_mbtis_choice1_count,
        "mbtis_choice2_count": total_mbtis_choice2_count,
        "poll": poll,
    }
    return render(request, template_name="vote/result.html", context=ctx)

#비회원 투표시 MBTI 기입 
def poll_nonusermbti(request, poll_id, nonuservote_id):
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        if choice_id == "M":
            NonUserVote.objects.filter(pk=nonuservote_id).update(gender="M")
        if choice_id == "W":
            NonUserVote.objects.filter(pk=nonuservote_id).update(gender="W")
        poll = get_object_or_404(Poll, id=poll_id)
        context = {
            "poll": poll,
            "mbti": ["INTP", "ESFJ"],
            "nonuservote_id": nonuservote_id,
            "loop_time": range(0, 2),
        }
        return render(request, "vote/detail3.html", context)

#비회원 투표시 투표 정보 전송
def poll_nonuserfinal(request, poll_id, nonuservote_id):
    choice_id = request.POST.get("choice")
    NonUserVote.objects.filter(pk=nonuservote_id).update(MBTI=str(choice_id))
    calcstat_url = reverse("vote:calcstat", args=[poll_id])
    return redirect(calcstat_url)