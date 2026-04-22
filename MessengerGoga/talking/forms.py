# Импорт модуля форм Django и моделей Author и Book
from django import forms
from .models import User, ChatMessage, Chat, ChatType

class UserFormReg(forms.ModelForm):
    username = forms.CharField(
        label = "Введи своё имя", 
        max_length=32
        )
    password = forms.CharField(
        label = "Введи свой пароль", 
        max_length=32,
        widget=forms.PasswordInput
        )
    #Dobavitj opisanije???
    class Meta:
        model = User
        fields = ['username', 'password']
    def save(self, commit=True):
        user = super().save(commit=False)
    
        # Хэшируем пароль!
        user.set_password(self.cleaned_data['password'])
    
        if commit:
            user.save()
        return user
    
class UserFormLogin(forms.ModelForm):
    username = forms.CharField(
        label = "Введи своё имя", 
        max_length=32
        )
    password = forms.CharField(
        label = "Введи свой пароль", 
        max_length=32,
        widget=forms.PasswordInput
        )
    class Meta:
        model = User
        fields = ['username', 'password']

class UserFormEdit(forms.ModelForm):
    username = forms.CharField(
        label = "Имя", 
        max_length=32
        )
    description = forms.CharField(
        label = "Описание",
        required = False
        )
    class Meta:
        model = User
        fields = ['username', 'description']
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    
    #     # Хэшируем пароль!
    #     user.set_password(self.cleaned_data['password'])
    
    #     if commit:
    #         user.save()
    #     return user





class ChatFormCreate(forms.ModelForm):
    name = forms.CharField(
        label="Название чата",
        max_length=72
    )
    description = forms.CharField(
        required=False,
        label="Описание чата",
        max_length=128,
    )
    chat_type = forms.ModelChoiceField(
        queryset=ChatType.objects.all(),
        label='Тип чата',
        empty_label="Выбери тип чата",  # Значение по умолчанию
    )

    class Meta:
        model = Chat
        fields = ['name', 'description', 'chat_type']

    def save(request, self, commit=True):
        lechat = super().save(commit=False)
        lechat.chat_creator = self.user

        if commit and lechat.chat_type.name!="ЛС":
            lechat.save()
        return lechat

class ChatFormEdit(forms.ModelForm):
    name = forms.CharField(
        label="Название чата",
        max_length=32
    )
    description = forms.CharField(
        required=False,
        label="Описание чата",
        max_length=128,
    )
    class Meta:
        model = Chat
        fields = ['name', 'description']



class ChatMessageForm(forms.ModelForm):
    message_words = forms.CharField(
        max_length=4096,
        label="Сообщение"
    )

    message_file = forms.CharField(
        label = "FILE_INPUT"
    )
    class Meta:
        model = ChatMessage
        fields = ['message_words', 'message_file']
    def save(request, self, commit=True):
        msg = super().save(commit=False)
        msg.chat = Chat.objects.get(id=self.scope["url_route"]["kwargs"]["room_name"])
        msg.user = self.user
        if commit:
            msg.save()
        return msg
        