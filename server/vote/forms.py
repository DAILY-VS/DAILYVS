from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    # nickname = forms.CharField(label='닉네임', max_length=20)
    # mbti = forms.ChoiceField(label='MBTI', choices=User.MBTI_set)
    # gender = forms.ChoiceField(label='성별', choices=User.GENDERS)
    
    class Meta:
        model = Comment
        fields = ['content']