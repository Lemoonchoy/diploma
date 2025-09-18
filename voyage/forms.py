from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите комментарий...'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["fio", "age", "photo", "married", "license"]
        widgets = {
            "fio": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите ФИО"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Возраст"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "married": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "license": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
