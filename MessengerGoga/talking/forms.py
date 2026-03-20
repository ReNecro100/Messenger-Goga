# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User, ChatMessage, Chat

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
    
        if commit:
            user.save()
        return user

class ChatMessageForm(forms.ModelForm):
    message_words = forms.CharField(
        max_length=4096,
        label="Сообщение"
    )
    class Meta:
        model = ChatMessage
        fields = ['message_words']
    def save(request, self, commit=True):
        msg = super().save(commit=False)
        msg.chat = Chat.objects.get(id=2)
        msg.user = self.user
        if commit:
            msg.save()
        return msg
        