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
        ("M", "남성(Man)"),
        ("W", "여성(Woman)"),
    ]

    gender = forms.ChoiceField(
        label="성별",
        choices=gender_choices,
        widget=forms.RadioSelect(attrs={"class": "radio-list"}),
    )

    MBTI_CHOICES = [
        ("INFP", "INFP"),
        ("ENFP", "ENFP"),
        ("INFJ", "INFJ"),
        ("ENFJ", "ENFJ"),
        ("INTJ", "INTJ"),
        ("ENTJ", "ENTJ"),
        ("INTP", "INTP"),
        ("ENTP", "ENTP"),
        ("ISFP", "ISFP"),
        ("ESFP", "ESFP"),
        ("ISFJ", "ISFJ"),
        ("ESFJ", "ESFJ"),
        ("ISTP", "ISTP"),
        ("ESTP", "ESTP"),
        ("ISTJ", "ISTJ"),
        ("ESTJ", "ESTJ"),
    ]

    mbti = forms.ChoiceField(
        label="MBTI",
        choices=MBTI_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "mbti", "nickname", "gender"]
        widgets = {
            "mbti": forms.Select(
                attrs={"class": "form-control", "placeholder": "MBTI (대문자로 ex.INFP)"}
            ),
            "nickname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "별명을 입력하세요"}
            ),
        }


class UserChangeForm(UserChangeForm):
        fields = ["username", "password1", "password2", "mbti", "nickname", "gender"]
        widgets = {
            "mbti": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "MBTI (대문자로 ex.INFP)"}
            ),
            "nickname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "별명을 입력하세요"}
            ),
        }

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
        fields = ["nickname", "mbti", "gender"]
        widgets = {
            "mbti": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "MBTI를 입력하세요"}
            ),
            "gender": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "성별을 입력하세요"}
            ),
        }
