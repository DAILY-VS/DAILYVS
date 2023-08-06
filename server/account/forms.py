from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        max_length=100,
        min_length=5,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "아이디를 입력하세요"}
        ),
    )
    password1 = forms.CharField(
        label="비밀번호",
        max_length=50,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호"}
        ),
    )
    password2 = forms.CharField(
        label="확인 비밀번호",
        max_length=50,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호 확인"}
        ),
    )
    gender_choices = [
        ("male", "남자"),
        ("female", "여자"),
    ]
    gender = forms.ChoiceField(
        label="성별",
        choices=gender_choices,
        widget=forms.RadioSelect(attrs={"class": "radio-list"}),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "mbti", "nickname", "gender"]
        widgets = {
            "mbti": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "MBTI를 입력하세요"}
            ),
            "nickname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "별명을 입력하세요"}
            ),
        }


class UserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ["nickname", "mbti", "gender"]
        widgets = {
            "mbti": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "MBTI를 입력하세요"}
            ),
            "gender": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "성별을 입력하세요"}
            ),
        }
