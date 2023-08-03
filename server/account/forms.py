from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    mbti = forms.CharField(max_length=4)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = forms.ChoiceField(choices=GENDERS)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'mbti', 'gender']