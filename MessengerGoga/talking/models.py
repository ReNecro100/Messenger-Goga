from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #username
    #password
    #date_joined
    description =models.TextField(
        verbose_name="Описание", 
        default=""
    )

class Chat(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name="Название",
        blank=False,
        unique=True
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания"
    )

    description = models.TextField(
        verbose_name="Описание", 
        blank=True
    )

    # Связь с автором (внешний ключ)
    chat_creator = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,
        related_name='chat_creator',
        verbose_name="Создатель чата"
    )

    #Чат, лс, канал
    chat_type = models.ForeignKey(
        'ChatType', 
        on_delete=models.CASCADE,
        verbose_name="Тип чата"
    )

class ChatType(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name="Название",
        blank=False,
        default=1,
        unique=True
    )
    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='message_sender',  # Обратная связь: author.books.all()
        verbose_name="Автор"
    )
    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='message_chat',  # Обратная связь: author.books.all()
        verbose_name="Чат"
    )
    sending_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата отправки"
    )
    message_words = models.CharField(
        max_length=4096,
        verbose_name="Сообщение",
    )
    message_file = models.BinaryField(
        verbose_name="Файл"
    )