from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Notation, UserProfile


class RequestForm(forms.Form):
    user_input = forms.CharField(label="Напиши что интересного произошло за сегодня...", max_length=100)
    is_public = forms.BooleanField(initial=False, required=False)
    tag_notion = forms.CharField(max_length=100, required=False)
    topic_notion = forms.CharField(max_length=100, required=False)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "city",
            "password1",
            "password2",
        ]


class NotationForm(forms.ModelForm):
    class Meta:
        model = Notation
        fields = ['topic_notion', 'tag_notion', 'content', 'is_public']  # Поля, которые вы хотите включить в форму.
        widgets = {
            'topic_notion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему заметки'}),
            'tag_notion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тег'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите содержимое заметки'}),
            # для чекбокса 'is_public' виджет по умолчанию подойдет, но вы можете настроить его также
        }
        labels = {
            'topic_notion': 'Тема заметки',
            'tag_notion': 'Тег',
            'content': 'Содержимое',
            'is_public': 'Публичная заметка',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']