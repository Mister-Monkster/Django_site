from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    is_verificated = models.BooleanField(verbose_name='Статус верификации', default=False,
                    help_text='Если стоит галочка - пользователь верифицирован, если нет - значит пользователь не прошел процедуру верификации')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'