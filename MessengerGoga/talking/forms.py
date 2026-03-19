# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(
        label = "Твой юзернейм", 
        max_length=150
        )
    email = forms.CharField(
        label="Твоё мыло"
    )
    password = forms.CharField(
        label = "Твой пароль", 
        max_length=32,
        widget=forms.PasswordInput
        )
    class Meta:
        model = User
        fields = ['username', 'email','password']
    def save(self, commit=True):
        user = super().save(commit=False)
    
        # Хэшируем пароль!
        user.set_password(self.cleaned_data['password'])
        print(self.cleaned_data['password'])
    
        if commit:
            user.save()
        return user
        