from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с авторизацией по email"""

    # Email как основное поле для входа
    email = models.EmailField(unique=True, verbose_name='Электронная почта')

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер телефона'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна'
    )

    # Указываем, что email используется для входа вместо username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username остаётся, но не используется для входа

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email