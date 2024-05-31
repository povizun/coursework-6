from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    is_banned = models.BooleanField(default=False, verbose_name='статус блокировки')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.last_name:
            return f"{self.last_name}"
        elif self.first_name:
            return f"{self.first_name}"
        else:
            return f"{self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('is_active', 'pk',)
        permissions = [
            ('can_edit_is_banned', 'Can edit is_banned'),
            ('can_view_all_users', 'Can view all users')
        ]
