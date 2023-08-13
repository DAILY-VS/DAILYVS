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

import random
import string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import smtplib

User = get_user_model()


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@login_required
def email_verification(request, user_id):
    user = get_object_or_404(User, id=user_id)
    code = generate_verification_code()
    print(code)
    try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()

            EMAIL_HOST_USER = 'songvv2014@gmail.com'
            EMAIL_HOST_PASSWORD = 'usrczzcpaxrcorqv'

            smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            subject = 'Daily-VS 이메일 인증코드'
            message = f'Daily-VS 이메일 인증코드는 다음과 같습니다. {code}'
            sender_email = EMAIL_HOST_USER
            recipient_email = user.email
            msg = f'Subject: {subject}\n\n{message}'
            smtp_server.sendmail(sender_email, recipient_email, msg.encode('utf-8'))

    except smtplib.SMTPException as e:
            print("An error occurred:", str(e))
    finally:
            smtp_server.quit()
    return render(request, "account/email_verification.html", {"user": user, "code": code})

def call(request):
    code = request.POST.get('code')  # Get the code from the form submission
    token = request.POST.get('token')
    if token == code:
            request.user.is_active = True
            request.user.save()
            return redirect("account:login")  # Redirect to login page after successful verification
    else:
            return render(request, "account/verification_error.html")

    

#회원가입
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            pk=str(user.pk)
            return redirect(f'/account/email_verification/{user.pk}/')
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