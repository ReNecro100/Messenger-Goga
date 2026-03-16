from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name="Имя"
    )

    password = models.CharField(
        max_length=32,
        verbose_name="Пароль"
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания"
    )

    description = description = models.TextField(
        verbose_name="Описание", 
        blank=True
    )