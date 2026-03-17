# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password']
        name = forms.CharField(
            label = "Your name", 
            max_length=32,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
            )
        password = forms.CharField(
            label = "Your password", 
            max_length=32,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
            )