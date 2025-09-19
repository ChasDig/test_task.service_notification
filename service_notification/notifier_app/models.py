from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Модель - Пользователь."""

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Номер телефона пользователя",
    )
    telegram_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Telegram chat_id пользователя",
    )

    def __str__(self):
        return self.username
