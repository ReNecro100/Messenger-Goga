# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','password']
        username = forms.CharField(
            label = "Твой юзернейм", 
            max_length=150
            )
        email = forms.CharField(
            label="Твоё мыло"
        )
        password = forms.CharField(
            label = "Твой пароль", 
            max_length=32
            )
        