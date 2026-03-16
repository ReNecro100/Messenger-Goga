# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password']
        name = forms.CharField(label = "Your name", max_length=32)
        password = forms.CharField(label = "Your password", max_length=32)