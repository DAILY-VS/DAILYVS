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
from django.core.serializers.json import DjangoJSONEncoder

# 메인페이지
def main(request):
    polls = Poll.objects.all()
    sort = request.GET.get("sort")
    promotion_polls = Poll.objects.filter(active=True).order_by("-pub_date")[:3]
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
        "promotion_polls": promotion_polls,
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


# 투표 게시글 좋아요
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
            
            if poll.poll_like.filter(id=user.id).exists():
                poll.poll_like.remove(user)
                message = "좋아요 취소"
            else:
                poll.poll_like.add(user)
                message = "좋아요"

            like_count = poll.poll_like.count()
            context = {"like_count": like_count, "message": message}
            return JsonResponse(context)
        return redirect('/')


# 유저 마이페이지
@login_required(login_url="/account/login/")  # 비로그인시 /mypage 막음
def mypage(request):
    polls = Poll.objects.all()
    page = request.GET.get("page")

    paginator = Paginator(polls, 4)
    uservotes = UserVote.objects.filter(user=request.user)
    polls_like= Poll.objects.filter(poll_like=request.user)

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
        "uservotes":uservotes,
        "polls_like":polls_like,
        "page_obj": page_obj,
        "paginator": paginator,
    }
    return render(request, "vote/mypage.html", context)


# 마이페이지 정보 수정
@login_required(login_url="/account/login/")  # 비로그인시 mypage/update 막음
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

#댓글 추가
@login_required
def comment_write_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    user_info = request.user  # 현재 로그인한 사용자
    content = request.POST.get('content')
    parent_comment_id = request.POST.get('parent_comment_id')  # 대댓글인 경우 부모 댓글의 ID를 받음
    
    if content:
        if parent_comment_id:  # 대댓글인 경우
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            comment = Comment.objects.create(
                poll=poll,
                content=content,
                user_info=user_info,
                parent_comment=parent_comment
            )
        else:  # 일반 댓글인 경우
            comment = Comment.objects.create(
                poll=poll,
                content=content,
                user_info=user_info,
            )
        poll.save()
        
        try:
            user_vote = UserVote.objects.get(user=request.user, poll=poll) #uservote에서 선택지 불러옴
            choice_text = user_vote.choice.choice_text
        except UserVote.DoesNotExist:
            user_vote = None
            choice_text = ""  # 또는 다른 기본값 설정
    
        comment_id = Comment.objects.last().pk
    
        data = {
            'nickname': user_info.nickname,
            'mbti': user_info.mbti,
            'gender': user_info.gender,
            'content': content,
            'created_at': comment.created_at.strftime("%Y년 %m월 %d일"),
            'comment_id': comment_id,
            'user_vote_choice_text': choice_text,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")
    else:
        return HttpResponse(status=400)  # Bad Request
    
#댓글 삭제
@login_required
def comment_delete_view(request, pk):
    poll = get_object_or_404(Poll, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.user_info:
        target_comment.delete()
        poll.save()
        data = {
            'comment_id': comment_id,
            'success': True
        }
    else:
        data = {
            'success': False,
            'error': '본인 댓글이 아닙니다.'
        }
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


# 계산 함수
def calculate_percentage(count, total_count):
    return int(count / total_count * 100) if total_count != 0 else 0

def calculate_statistics(queryset, choices):
    counts = [queryset.filter(choice_id=choice_id).count() for choice_id in choices]
    total_count = sum(counts)
    return counts, total_count

def calculate_mbti_statistics(queryset, choices, mbtis):
    mbti_counts = [[queryset.filter(choice_id=choice_id, user__mbti=mbti).count() for mbti in mbtis] for choice_id in choices]
    total_mbtis_count = [sum(column) for column in zip(*mbti_counts)]
    return mbti_counts, total_mbtis_count

def calcstat(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    comments = Comment.objects.filter(poll_id=poll_id)
    
    if request.user.is_authenticated:
        user_votes = request.user.voted_polls.all()
    else:
        user_votes = None
    
    mbtis = [
        "ISTJ", "ISFJ", "INFJ", "INTJ",
        "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP",
        "ESTJ", "ESFJ", "ENFJ", "ENTJ",
    ]

    user_poll = UserVote.objects.filter(poll__pk=poll_id)
    nonuser_poll = NonUserVote.objects.filter(poll__pk=poll_id, MBTI__isnull=False, gender__isnull=False)

    user_choices = [2 * poll_id - 1, 2 * poll_id]
    nonuser_choices = [2 * poll_id - 1, 2 * poll_id]

    user_choice_counts, user_total_count = calculate_statistics(user_poll, user_choices)
    nonuser_choice_counts, nonuser_total_count = calculate_statistics(nonuser_poll, nonuser_choices)

    total_count = user_total_count + nonuser_total_count

    user_man_poll = user_poll.filter(user__gender="M")
    user_woman_poll = user_poll.filter(user__gender="W")

    nonuser_man_poll = nonuser_poll.filter(gender="M")
    nonuser_woman_poll = nonuser_poll.filter(gender="W")

    user_man_choice_counts, user_man_total_count = calculate_statistics(user_man_poll, user_choices)
    user_woman_choice_counts, user_woman_total_count = calculate_statistics(user_woman_poll, user_choices)
    
    nonuser_man_choice_counts, nonuser_man_total_count = calculate_statistics(nonuser_man_poll, nonuser_choices)
    nonuser_woman_choice_counts, nonuser_woman_total_count = calculate_statistics(nonuser_woman_poll, nonuser_choices)

    total_man_count = user_man_total_count + nonuser_man_total_count
    total_woman_count = user_woman_total_count + nonuser_woman_total_count

    user_mbtis_choice_counts, user_mbtis_total_counts = calculate_mbti_statistics(user_poll, user_choices, mbtis)
    nonuser_mbtis_choice_counts, nonuser_mbtis_total_counts = calculate_mbti_statistics(nonuser_poll, nonuser_choices, mbtis)

    total_mbtis_count = [user + nonuser for user, nonuser in zip(user_mbtis_total_counts, nonuser_mbtis_total_counts)]

    choice1_percentage = calculate_percentage(user_choice_counts[0] + nonuser_choice_counts[0], total_count)
    choice2_percentage = calculate_percentage(user_choice_counts[1] + nonuser_choice_counts[1], total_count)

    choice1_man_percentage = calculate_percentage(user_man_choice_counts[0] + nonuser_man_choice_counts[0], total_man_count)
    choice2_man_percentage = calculate_percentage(user_man_choice_counts[1] + nonuser_man_choice_counts[1], total_man_count)

    choice1_woman_percentage = calculate_percentage(user_woman_choice_counts[0] + nonuser_woman_choice_counts[0], total_woman_count)
    choice2_woman_percentage = calculate_percentage(user_woman_choice_counts[1] + nonuser_woman_choice_counts[1], total_woman_count)

    user_mbtis_choice1_counts, _ = calculate_mbti_statistics(user_poll, user_choices[:1], mbtis)
    nonuser_mbtis_choice1_counts, _ = calculate_mbti_statistics(nonuser_poll, nonuser_choices[:1], mbtis)
    user_mbtis_choice1_percentage = [calculate_percentage(user + nonuser, total) for user, nonuser, total in zip(user_mbtis_choice1_counts[0], nonuser_mbtis_choice1_counts[0], total_mbtis_count)]

    e_choice1_count = sum(user_mbtis_choice1_counts[0][:2]) + sum(nonuser_mbtis_choice1_counts[0][:2])
    e_total_count = sum(total_mbtis_count[:2])
    e_choice1_percentage = calculate_percentage(e_choice1_count, e_total_count)
    e_choice2_percentage = 100 - e_choice1_percentage
    
    i_choice1_count = sum(user_mbtis_choice1_counts[0][2:6]) + sum(nonuser_mbtis_choice1_counts[0][2:6])
    i_total_count = sum(total_mbtis_count[2:6])
    i_choice1_percentage = calculate_percentage(i_choice1_count, i_total_count)
    i_choice2_percentage = 100 - i_choice1_percentage

    n_choice1_count = sum(user_mbtis_choice1_counts[0][2:4] + user_mbtis_choice1_counts[0][6:8]) + sum(nonuser_mbtis_choice1_counts[0][2:4] + nonuser_mbtis_choice1_counts[0][6:8])
    n_total_count = sum(total_mbtis_count[2:4] + total_mbtis_count[6:8])
    n_choice1_percentage = calculate_percentage(n_choice1_count, n_total_count)
    n_choice2_percentage = 100 - n_choice1_percentage

    s_choice1_count = sum(user_mbtis_choice1_counts[0][:2] + user_mbtis_choice1_counts[0][4:6]) + sum(nonuser_mbtis_choice1_counts[0][:2] + nonuser_mbtis_choice1_counts[0][4:6])
    s_total_count = sum(total_mbtis_count[:2] + total_mbtis_count[4:6])
    s_choice1_percentage = calculate_percentage(s_choice1_count, s_total_count)
    s_choice2_percentage = 100 - s_choice1_percentage

    t_choice1_count = sum(user_mbtis_choice1_counts[0][:2] + user_mbtis_choice1_counts[0][6:8]) + sum(nonuser_mbtis_choice1_counts[0][:2] + nonuser_mbtis_choice1_counts[0][6:8])
    t_total_count = sum(total_mbtis_count[:2] + total_mbtis_count[6:8])
    t_choice1_percentage = calculate_percentage(t_choice1_count, t_total_count)
    t_choice2_percentage = 100 - t_choice1_percentage

    f_choice1_count = sum(user_mbtis_choice1_counts[0][2:6]) + sum(nonuser_mbtis_choice1_counts[0][2:6])
    f_total_count = sum(total_mbtis_count[2:6])
    f_choice1_percentage = calculate_percentage(f_choice1_count, f_total_count)
    f_choice2_percentage = 100 - f_choice1_percentage

    j_choice1_count = sum(user_mbtis_choice1_counts[0][:2] + user_mbtis_choice1_counts[0][4:6]) + sum(nonuser_mbtis_choice1_counts[0][:2] + nonuser_mbtis_choice1_counts[0][4:6])
    j_total_count = sum(total_mbtis_count[:2] + total_mbtis_count[4:6])
    j_choice1_percentage = calculate_percentage(j_choice1_count, j_total_count)
    j_choice2_percentage = 100 - j_choice1_percentage

    p_choice1_count = sum(user_mbtis_choice1_counts[0][2:4] + user_mbtis_choice1_counts[0][6:8]) + sum(nonuser_mbtis_choice1_counts[0][2:4] + nonuser_mbtis_choice1_counts[0][6:8])
    p_total_count = sum(total_mbtis_count[2:4] + total_mbtis_count[6:8])
    p_choice1_percentage = calculate_percentage(p_choice1_count, p_total_count)
    p_choice2_percentage = 100 - p_choice1_percentage

    ctx = {
        "total_count": total_count,
        "choice1_count": user_choice_counts[0] + nonuser_choice_counts[0],
        "choice2_count": user_choice_counts[1] + nonuser_choice_counts[1],
        "choice1_percentage": choice1_percentage,
        "choice2_percentage": choice2_percentage,
        "man_count": total_man_count,
        "man_choice1_count": user_man_choice_counts[0] + nonuser_man_choice_counts[0],
        "man_choice2_count": user_man_choice_counts[1] + nonuser_man_choice_counts[1],
        "woman_count": total_woman_count,
        "woman_choice1_count": user_woman_choice_counts[0] + nonuser_woman_choice_counts[0],
        "woman_choice2_count": user_woman_choice_counts[1] + nonuser_woman_choice_counts[1],
        "choice1_man_percentage": choice1_man_percentage,
        "choice2_man_percentage": choice2_man_percentage,
        "choice1_woman_percentage": choice1_woman_percentage,
        "choice2_woman_percentage": choice2_woman_percentage,
        "mbtis": mbtis,
        "mbtis_count": total_mbtis_count,
        "mbtis_choice1_count": user_mbtis_choice_counts[0] + nonuser_mbtis_choice_counts[0],
        "mbtis_choice2_count": user_mbtis_choice_counts[1] + nonuser_mbtis_choice_counts[1],
        "e_choice1_percentage": e_choice1_percentage,
        "e_choice2_percentage": e_choice2_percentage,
        "i_choice1_percentage": i_choice1_percentage,
        "i_choice2_percentage": i_choice2_percentage,
        "s_choice1_percentage": s_choice1_percentage,
        "s_choice2_percentage": s_choice2_percentage,
        "n_choice1_percentage": n_choice1_percentage,
        "n_choice2_percentage": n_choice2_percentage,
        "t_choice1_percentage": t_choice1_percentage,
        "t_choice2_percentage": t_choice2_percentage,
        "f_choice1_percentage": f_choice1_percentage,
        "f_choice2_percentage": f_choice2_percentage,
        "p_choice1_percentage": p_choice1_percentage,
        "p_choice2_percentage": p_choice2_percentage,
        "j_choice1_percentage": j_choice1_percentage,
        "j_choice2_percentage": j_choice2_percentage,
        "poll": poll,
        'comments': comments,
        'user_votes': user_votes,
    }
    
    return render(request, template_name="vote/result.html", context=ctx)


# 투표 시 회원, 비회원 구분 (비회원일시 성별 기입)
def classifyuser(request, poll_id):
    if request.method == "POST":
        poll = get_object_or_404(Poll, pk=poll_id)
        choice_id = request.POST.get("choice")  # 뷰에서 선택 불러옴
        user = request.user
        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            try:
                vote = UserVote(user=request.user, poll=poll, choice=choice)
                vote.save()
                user.voted_polls.add(poll_id)
                calcstat_url = reverse("vote:calcstat", args=[poll_id])
                voted_polls = user.voted_polls.all()
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


# 비회원 투표시 MBTI 기입
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


# 비회원 투표시 투표 정보 전송
def poll_nonuserfinal(request, poll_id, nonuservote_id):
    choice_id = request.POST.get("choice")
    NonUserVote.objects.filter(pk=nonuservote_id).update(MBTI=str(choice_id))
    calcstat_url = reverse("vote:calcstat", args=[poll_id])
    return redirect(calcstat_url)
