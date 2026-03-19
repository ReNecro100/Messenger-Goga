from django.db import models
from django.contrib.auth.models import User as UserModel

# Create your models here.
# class User(models.Model):
#     name = models.CharField(
#         max_length=32,
#         verbose_name="Имя",
#         blank=False,
#         unique=True
#     )

#     password = models.CharField(
#         max_length=32,
#         verbose_name="Пароль",
#         blank=False,
#         unique=True
#     )

#     creation_date = models.DateTimeField(
#         auto_now=True,
#         verbose_name="Дата создания"
#     )

#     description = description = models.TextField(
#         verbose_name="Описание", 
#         blank=True
#     )
class User(UserModel):
    #username
    #password
    #date_joined
    description = description = models.TextField(
        verbose_name="Описание", 
        default=""
    )

class Chats(models.Model):
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

    description = description = models.TextField(
        verbose_name="Описание", 
        blank=True
    )

    # Связь с автором (внешний ключ)
    chat_creator = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='talkinb',  # Обратная связь: author.books.all()
        verbose_name="Создатель чата"
    )

    #Чат - 1, ЛС - 2, Канал - 3
    ChatDMChannel = models.CharField( 
        max_length=1,
        verbose_name="Чат, лс или канал",
        blank=False
    )

class ChatMessages(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='talking',  # Обратная связь: author.books.all()
        verbose_name="Автор"
    )
    chat = models.ForeignKey(
        Chats, 
        on_delete=models.CASCADE,  # При удалении автора удаляются все его книги
        related_name='talking',  # Обратная связь: author.books.all()
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