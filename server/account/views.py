from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import SignupForm 
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from vote.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import User

User = get_user_model()

#회원가입
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            return redirect("/")
        else:
            ctx = {
                "form": form,
            }
            return render(request, "account/signup.html", context=ctx)
    else:
        form = SignupForm()
        ctx = {
            "form": form,
        }
        return render(request, template_name="account/signup.html", context=ctx)
    
#로그인
def login(request):  
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect("/")
        else:
            wrong_password = True  # 비밀번호가 틀렸을 때 변수를 설정하여 템플릿으로 전달
            context = {
                "form": form,
                "wrong_password": wrong_password,  # 변수를 템플릿으로 전달
            }
            return render(request, "account/login.html", context=context)
    else:
        form = AuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "account/login.html", context=context)

#로그아웃
def logout(request):  
    auth.logout(request)
    return redirect("/")

#비밀번호 변경
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 변경 후 로그인 상태 유지
            return redirect("vote:mypage")  # 변경 후 이동할 페이지
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "account/change_password.html", context)

#회원탈퇴
class UserDeleteView(DeleteView):
    model = User
    template_name = "account/delete.html"
    success_url = reverse_lazy("vote:mypage")
    form_class = UserDeleteForm

    def get_object(self, queryset=None):
        return self.request.user
