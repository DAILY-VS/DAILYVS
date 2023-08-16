import json
import numpy as np
import random
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
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist



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
    random_poll = random.choice(polls) if polls.exists() else None
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
        "random_poll": random_poll,
    }

    return render(request, "vote/main.html", context)

# 투표 디테일 페이지
def poll_detail(request, poll_id):
    user = request.user
    poll = get_object_or_404(Poll, id=poll_id)

    if user.is_authenticated and user.voted_polls.filter(id=poll_id).exists():
        uservote=UserVote.objects.filter(poll_id=poll_id).get(user=user)
        calcstat_url = reverse("vote:calcstat", args=[poll_id,uservote.id,0])
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


# 투표 게시글 좋아요 초기 검사
def get_like_status(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return JsonResponse({"error": "해당 투표가 존재하지 않습니다."}, status=404)

    user = request.user
    user_likes_poll = False

    if request.user.is_authenticated:
        if poll.poll_like.filter(id=user.id).exists():
            user_likes_poll = True

    context = {"user_likes_poll": user_likes_poll}
    return JsonResponse(context)


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

        user = request.user
        if request.user.is_authenticated:
            if poll.poll_like.filter(id=user.id).exists():
                poll.poll_like.remove(user)
                message = "좋아요 취소"
                user_likes_poll = False
            else:
                poll.poll_like.add(user)
                message = "좋아요"
                user_likes_poll = True

            like_count = poll.poll_like.count()
            context = {
                "like_count": like_count,
                "message": message,
                "user_likes_poll": user_likes_poll,
            }
            return JsonResponse(context)
        return redirect("/")


@login_required(login_url="/account/login/")  # 비로그인시 /mypage 막음
def mypage(request):
    polls = Poll.objects.all()
    page = request.GET.get("page")
    paginator = Paginator(polls, 4)
    uservotes = UserVote.objects.filter(user=request.user)
    polls_like = Poll.objects.filter(poll_like=request.user)
    page_obj_polls_like = Paginator(polls_like, 3)  # 페이지 번호를 뷰에서 처리

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
        "uservotes": uservotes,
        "page_obj_polls_like": page_obj_polls_like,
        "polls_like": polls_like,
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


# 댓글 쓰기
@login_required
def comment_write_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    user_info = request.user  # 현재 로그인한 사용자
    content = request.POST.get("content")
    parent_comment_id = request.POST.get("parent_comment_id")
    if content:
        if parent_comment_id:  # 대댓글인 경우
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            comment = Comment.objects.create(
                poll=poll,
                content=content,
                user_info=user_info,
                parent_comment=parent_comment,
            )
            parent_comment_data = {
                "nickname": parent_comment.user_info.nickname,
                "mbti": parent_comment.user_info.mbti,
                "gender": parent_comment.user_info.gender,
                "content": parent_comment.content,
                "created_at": parent_comment.created_at.strftime("%Y년 %m월 %d일"),
                "comment_id": parent_comment.pk,
            }
        else:  # 일반 댓글인 경우
            comment = Comment.objects.create(
                poll=poll,
                content=content,
                user_info=user_info,
            )
            parent_comment_data = None

        poll.update_comments_count()  # 댓글 수 업데이트
        poll.save()

        try:
            user_vote = UserVote.objects.get(
                user=request.user, poll=poll
            )  # uservote에서 선택지 불러옴
            choice_text = user_vote.choice.choice_text
        except UserVote.DoesNotExist:
            user_vote = None
            choice_text = ""  # 또는 다른 기본값 설정

        comment_id = comment.pk

        data = {
            "nickname": user_info.nickname,
            "mbti": user_info.mbti,
            "gender": user_info.gender,
            "content": content,
            "created_at": comment.created_at.strftime("%Y년 %m월 %d일"),
            "comment_id": comment_id,
            "choice": choice_text,
        }
        if parent_comment_data:
            data["parent_comment"] = parent_comment_data

        return HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
        )


# 댓글 삭제
@login_required
def comment_delete_view(request, pk):
    poll = get_object_or_404(Poll, id=pk)
    comment_id = request.POST.get("comment_id")
    target_comment = Comment.objects.get(pk=comment_id)

    if request.user == target_comment.user_info:
        target_comment.delete()
        poll.save()
        data = {"comment_id": comment_id, "success": True}
    else:
        data = {"success": False, "error": "본인 댓글이 아닙니다."}
    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json"
    )


# 대댓글 수 파악
def calculate_nested_count(request, comment_id):
    nested_count = Comment.objects.filter(parent_comment_id=comment_id).count()
    return JsonResponse({"nested_count": nested_count})


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
                poll_result, created = Poll_Result.objects.get_or_create(
                    poll_id=poll_id
                )
                poll_result.total += 1
                if user.gender == "M":
                    poll_result.choice1_man += (
                        1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                    )
                    poll_result.choice2_man += (
                        1 if int(choice_id) == 2 * (poll_id) else 0
                    )
                    print(str(poll_result.choice1_man))
                elif user.gender == "W":
                    poll_result.choice1_woman += (
                        1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                    )
                    poll_result.choice2_woman += (
                        1 if int(choice_id) == 2 * (poll_id) else 0
                    )
                for letter in user.mbti:
                    if letter == "E":
                        poll_result.choice1_E += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_E += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "I":
                        poll_result.choice1_I += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_I += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "S":
                        poll_result.choice1_S += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_S += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "N":
                        poll_result.choice1_N += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_N += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "T":
                        poll_result.choice1_T += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_T += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "F":
                        poll_result.choice1_F += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_F += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "J":
                        poll_result.choice1_J += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_J += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                    elif letter == "P":
                        poll_result.choice1_P += (
                            1 if int(choice_id) == 2 * (poll_id) - 1 else 0
                        )
                        poll_result.choice2_P += (
                            1 if int(choice_id) == 2 * (poll_id) else 0
                        )
                poll_result.save()
                calcstat_url = reverse("vote:calcstat", args=[poll_id,vote.id,0])
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
    else:
        return redirect("/")


# 회원/비회원 투표 통계 계산 및 결과 페이지
def calcstat(request, poll_id,uservote_id,nonuservote_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    comments = Comment.objects.filter(poll_id=poll_id)
    if request.user.is_authenticated:
        user_votes = UserVote.objects.filter(user=request.user)
    else:
        user_votes = None  # 또는 user_votes = UserVote.objects.none()

    poll_result = Poll_Result.objects.get(poll_id=poll_id)

    total_count = poll_result.total

    choice_1 = poll_result.choice1_man + poll_result.choice1_woman
    choice_2 = poll_result.choice2_man + poll_result.choice2_woman

    choice1_percentage = int(np.round(choice_1 / total_count * 100))
    choice2_percentage = int(np.round(choice_2 / total_count * 100))

    choice1_man_percentage = (
        (
            np.round(
                poll_result.choice1_man
                / (poll_result.choice1_man + poll_result.choice2_man)
                * 100,
                1,
            )
        )
        if (poll_result.choice1_man + poll_result.choice2_man) != 0
        else 0
    )
    choice2_man_percentage = (
        (
            np.round(
                poll_result.choice2_man
                / (poll_result.choice1_man + poll_result.choice2_man)
                * 100,
                1,
            )
        )
        if (poll_result.choice1_man + poll_result.choice2_man) != 0
        else 0
    )
    choice1_woman_percentage = (
        (
            np.round(
                poll_result.choice1_woman
                / (poll_result.choice1_woman + poll_result.choice2_woman)
                * 100,
                1,
            )
        )
        if (poll_result.choice1_woman + poll_result.choice2_woman) != 0
        else 0
    )
    choice2_woman_percentage = (
        (
            np.round(
                poll_result.choice2_woman
                / (poll_result.choice1_woman + poll_result.choice2_woman)
                * 100,
                1,
            )
        )
        if (poll_result.choice1_woman + poll_result.choice2_woman) != 0
        else 0
    )

    e_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_E
                / (poll_result.choice1_E + poll_result.choice2_E)
                * 100
            )
        )
        if (poll_result.choice1_E + poll_result.choice2_E) != 0
        else 0
    )
    e_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_E
                / (poll_result.choice1_E + poll_result.choice2_E)
                * 100
            )
        )
        if (poll_result.choice1_E + poll_result.choice2_E) != 0
        else 0
    )
    i_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_I
                / (poll_result.choice1_I + poll_result.choice2_I)
                * 100
            )
        )
        if (poll_result.choice1_I + poll_result.choice2_I) != 0
        else 0
    )
    i_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_I
                / (poll_result.choice1_I + poll_result.choice2_I)
                * 100
            )
        )
        if (poll_result.choice1_I + poll_result.choice2_I) != 0
        else 0
    )

    n_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_N
                / (poll_result.choice1_N + poll_result.choice2_N)
                * 100
            )
        )
        if (poll_result.choice1_N + poll_result.choice2_N) != 0
        else 0
    )
    n_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_N
                / (poll_result.choice1_N + poll_result.choice2_N)
                * 100
            )
        )
        if (poll_result.choice1_N + poll_result.choice2_N) != 0
        else 0
    )
    s_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_S
                / (poll_result.choice1_S + poll_result.choice2_S)
                * 100
            )
        )
        if (poll_result.choice1_S + poll_result.choice2_S) != 0
        else 0
    )
    s_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_S
                / (poll_result.choice1_S + poll_result.choice2_S)
                * 100
            )
        )
        if (poll_result.choice1_S + poll_result.choice2_S) != 0
        else 0
    )

    t_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_T
                / (poll_result.choice1_T + poll_result.choice2_T)
                * 100
            )
        )
        if (poll_result.choice1_T + poll_result.choice2_T) != 0
        else 0
    )
    t_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_T
                / (poll_result.choice1_T + poll_result.choice2_T)
                * 100
            )
        )
        if (poll_result.choice1_T + poll_result.choice2_T) != 0
        else 0
    )
    f_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_F
                / (poll_result.choice1_F + poll_result.choice2_F)
                * 100
            )
        )
        if (poll_result.choice1_F + poll_result.choice2_F) != 0
        else 0
    )
    f_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_F
                / (poll_result.choice1_F + poll_result.choice2_F)
                * 100
            )
        )
        if (poll_result.choice1_F + poll_result.choice2_F) != 0
        else 0
    )

    p_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_P
                / (poll_result.choice1_P + poll_result.choice2_P)
                * 100
            )
        )
        if (poll_result.choice1_P + poll_result.choice2_P) != 0
        else 0
    )
    p_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_P
                / (poll_result.choice1_P + poll_result.choice2_P)
                * 100
            )
        )
        if (poll_result.choice1_P + poll_result.choice2_P) != 0
        else 0
    )
    j_choice1_percentage = (
        (
            np.round(
                poll_result.choice1_J
                / (poll_result.choice1_J + poll_result.choice2_J)
                * 100
            )
        )
        if (poll_result.choice1_J + poll_result.choice2_J) != 0
        else 0
    )
    j_choice2_percentage = (
        (
            np.round(
                poll_result.choice2_J
                / (poll_result.choice1_J + poll_result.choice2_J)
                * 100
            )
        )
        if (poll_result.choice1_J + poll_result.choice2_J) != 0
        else 0
    )
    
    dict= {}    
    try :
        uservote = UserVote.objects.get(id=uservote_id)
        user=uservote.user
        if uservote.choice.id == 1 :
            if user.gender == 'M' :
                dict['남자'] = choice1_man_percentage
            elif user.gender == 'W' :
                dict['여자'] = choice1_woman_percentage
            for letter in user.mbti:
                if letter == 'E':
                    dict['E'] = e_choice1_percentage
                elif letter == 'I':
                    dict['I'] = i_choice1_percentage
                elif letter == 'S':
                    dict['S'] = s_choice1_percentage
                elif letter == 'N':
                    dict['N'] = n_choice1_percentage
                elif letter == 'T':
                    dict['T'] = t_choice1_percentage
                elif letter == 'F':
                    dict['F'] = f_choice1_percentage
                elif letter == 'P':
                    dict['P'] = p_choice1_percentage
                elif letter == 'J':
                    dict['J'] = j_choice1_percentage
        if uservote.choice.id == 2:
            if user.gender == 'M' :
                dict['남자'] = choice2_man_percentage
            elif user.gender == 'W' :
                dict['여자'] = choice2_woman_percentage
            for letter in user.mbti:
                if letter == 'E':
                    dict['E'] = e_choice2_percentage
                elif letter == 'I':
                    dict['I'] = i_choice2_percentage
                elif letter == 'S':
                    dict['S'] = s_choice2_percentage
                elif letter == 'N':
                    n_choice2_percentage = 10
                    dict['N'] = n_choice2_percentage
                elif letter == 'T':
                    dict['T'] = t_choice2_percentage
                elif letter == 'F':
                    dict['F'] = f_choice2_percentage
                elif letter == 'P':
                    dict['P'] = p_choice2_percentage
                elif letter == 'J':
                    dict['J'] = j_choice2_percentage
    except (ObjectDoesNotExist): 
        nonuservote = NonUserVote.objects.get(id=nonuservote_id)
        nonuser_gender=nonuservote.gender
        nonuser_mbti=nonuservote.MBTI
        if nonuservote.choice.id == 1 :
            if nonuser_gender == 'M' :
                dict['남자'] = choice1_man_percentage
            elif nonuser_gender == 'W' :
                dict['여자'] = choice1_woman_percentage
            for letter in nonuser_mbti:
                if letter == 'E':
                    dict['E'] = e_choice1_percentage
                elif letter == 'I':
                    dict['I'] = i_choice1_percentage
                elif letter == 'S':
                    dict['S'] = s_choice1_percentage
                elif letter == 'N':
                    dict['N'] = n_choice1_percentage
                elif letter == 'T':
                    dict['T'] = t_choice1_percentage
                elif letter == 'F':
                    dict['F'] = f_choice1_percentage
                elif letter == 'P':
                    dict['P'] = p_choice1_percentage
                elif letter == 'J':
                    dict['J'] = j_choice1_percentage
        if nonuservote.choice.id == 2:
            if nonuser_gender == 'M' :
                dict['남자'] = choice2_man_percentage
            elif nonuser_gender == 'W' :
                dict['여자'] = choice2_woman_percentage
            for letter in nonuser_mbti:
                if letter == 'E':
                    dict['E'] = e_choice2_percentage
                elif letter == 'I':
                    dict['I'] = i_choice2_percentage
                elif letter == 'S':
                    dict['S'] = s_choice2_percentage
                elif letter == 'N':
                    dict['N'] = n_choice2_percentage
                elif letter == 'T':
                    dict['T'] = t_choice2_percentage
                elif letter == 'F':
                    dict['F'] = f_choice2_percentage
                elif letter == 'P':
                    dict['P'] = p_choice2_percentage
                elif letter == 'J':
                    dict['J'] = j_choice2_percentage
    print(dict)
    minimum_key = min(dict,key=dict.get)
    minimum_value= dict[min(dict,key=dict.get)]

    ctx = {
        "total_count": total_count,
        # "choice1_count": total_choice1_count,
        # "choice2_count": total_choice2_count,
        "choice1_percentage": choice1_percentage,
        "choice2_percentage": choice2_percentage,
        # "man_count": total_man_count,
        # "man_choice1_count": total_man_choice1_count,
        # "man_choice2_count": total_man_choice2_count,
        # "woman_count": total_woman_count,
        # "woman_choice1_count": total_woman_choice1_count,
        # "woman_choice2_count": total_woman_choice2_count,
        "choice1_man_percentage": choice1_man_percentage,
        "choice2_man_percentage": choice2_man_percentage,
        "choice1_woman_percentage": choice1_woman_percentage,
        "choice2_woman_percentage": choice2_woman_percentage,
        # "mbtis_count": total_mbtis_count,
        # "mbtis_choice1_count": total_mbtis_choice1_count,
        # "mbtis_choice2_count": total_mbtis_choice2_count,
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
        "comments": comments,
        "user_votes": user_votes,
        "minimum_key": minimum_key,
        "minimum_value":100 - minimum_value,
    }
    ##################################################################################
    
    return render(request, template_name="vote/result.html", context=ctx)


# 비회원 투표시 MBTI 기입
def poll_nonusermbti(request, poll_id, nonuservote_id):
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        selected_mbti = request.POST.get("selected_mbti")
        mbti_combination = selected_mbti

        nonuser_vote = NonUserVote.objects.get(pk=nonuservote_id)
        nonuser_vote.MBTI = mbti_combination
        nonuser_vote.save()

        if choice_id == "M":
            NonUserVote.objects.filter(pk=nonuservote_id).update(gender="M")
        if choice_id == "W":
            NonUserVote.objects.filter(pk=nonuservote_id).update(gender="W")

        poll = get_object_or_404(Poll, id=poll_id)
        context = {
            "poll": poll,
            "mbti": [],  # 여기에 MBTI 리스트 추가
            "nonuservote_id": nonuservote_id,
            "loop_time": range(0, 2),
        }
        return render(request, "vote/detail3.html", context)
    else:
        return redirect("/")


# 비회원 투표시 투표 정보 전송
def poll_nonuserfinal(request, poll_id, nonuservote_id):
    if request.method == "POST":
        selected_mbti = request.POST.get("selected_mbti")
        NonUserVote.objects.filter(pk=nonuservote_id).update(MBTI=selected_mbti)
        nonuservote = NonUserVote.objects.get(id=nonuservote_id)
        poll_result, created = Poll_Result.objects.get_or_create(poll_id=poll_id)
        poll_result.total += 1
        if nonuservote.gender == "M":
            poll_result.choice1_man += (
                1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
            )
            poll_result.choice2_man += (
                1 if nonuservote.choice_id == 2 * (poll_id) else 0
            )
        elif nonuservote.gender == "W":
            poll_result.choice1_woman += (
                1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
            )
            poll_result.choice2_woman += (
                1 if nonuservote.choice_id == 2 * (poll_id) else 0
            )
        for letter in selected_mbti:
            if letter == "E":
                poll_result.choice1_E += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_E += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "I":
                poll_result.choice1_I += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_I += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "S":
                poll_result.choice1_S += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_S += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "N":
                poll_result.choice1_N += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_N += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "T":
                poll_result.choice1_T += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_T += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "F":
                poll_result.choice1_F += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_F += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "J":
                poll_result.choice1_J += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_J += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
            elif letter == "P":
                poll_result.choice1_P += (
                    1 if nonuservote.choice_id == 2 * (poll_id) - 1 else 0
                )
                poll_result.choice2_P += (
                    1 if nonuservote.choice_id == 2 * (poll_id) else 0
                )
        poll_result.save()
        calcstat_url = reverse("vote:calcstat", args=[poll_id,0,nonuservote_id])
        return redirect(calcstat_url)
    else:
        return redirect("/")

def fortune(request):
    return render(request, "vote/main/main-fortune.html")
