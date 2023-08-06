from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class SignupForm(UserCreationForm): #회원가입
    username = forms.CharField(label='아이디', max_length=50, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','mbti','gender','nickname']
        
class UserChangeForm(UserChangeForm): #마이페이지 정보 수정
    password = None
    class Meta:
        model = get_user_model()
        fields = ['nickname','mbti','gender']