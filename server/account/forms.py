from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class SignupForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=100, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','mbti','gender','nickname']
        
class UserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['nickname','mbti','gender']


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []