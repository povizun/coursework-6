from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    last_name = models.CharField(max_length=50, verbose_name='фамилия', **NULLABLE)
    first_name = models.CharField(max_length=50, verbose_name='имя')
    middle_name = models.CharField(max_length=50, verbose_name='отчество', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    creator = models.ForeignKey(User, verbose_name='создатель', on_delete=models.RESTRICT, **NULLABLE)

    def __str__(self):
        if self.first_name and self.last_name and self.middle_name:
            return f"{self.first_name} {self.last_name} {self.middle_name}"
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name and self.middle_name:
            return f"{self.first_name} {self.middle_name}"
        elif self.last_name and self.middle_name:
            return f"{self.last_name} {self.middle_name}"
        elif self.first_name:
            return f"{self.first_name}"
        elif self.last_name:
            return f"{self.last_name}"
        elif self.middle_name:
            return f"{self.middle_name}"
        else:
            return f"{self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    creator = models.ForeignKey(User, verbose_name='создатель', on_delete=models.RESTRICT, **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    class StatusOfMailing(models.TextChoices):
        NEW = 'Новая', _('Новая')
        LAUNCHED = 'Запущена', _('Запущена')
        FINISHED = 'Завершена', _('Завершена')

    first_sent_at = models.DateTimeField(**NULLABLE, verbose_name='дата первой отправки')
    frequency = models.ForeignKey('Frequency', verbose_name='частота отправки рассылки', on_delete=models.RESTRICT)
    status = models.CharField(verbose_name='статус рассылки', choices=StatusOfMailing, default=StatusOfMailing.NEW)
    client_list = models.ManyToManyField('Client', verbose_name='список клиентов')
    message_to_send = models.ForeignKey('Message', verbose_name='сообщение для отправки', on_delete=models.RESTRICT)
    creator = models.ForeignKey(User, verbose_name='создатель', on_delete=models.RESTRICT, **NULLABLE)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_view_all_mailings', 'Can view all mailings'),
            ('can_change_status', 'Can change status of all mailings')
        ]


class MailingAttempt(models.Model):
    last_attempt = models.DateTimeField(auto_now=True, verbose_name='дата последней попытки')
    is_success = models.BooleanField(**NULLABLE, verbose_name='успешность последней попытки')
    server_answer = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')
    mailing = models.ForeignKey('Mailing', verbose_name='рассылка', on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.last_attempt} {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'


class Frequency(models.Model):
    name = models.CharField(max_length=50, verbose_name='частота отправки')
    days_until_next_mailing = models.IntegerField(verbose_name='количество дней до следующей отправки')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Частота рассылки'
        verbose_name_plural = 'Частоты рассылки'


class BlogPost(models.Model):
    title = models.CharField(max_length=50, verbose_name='тема поста')
    body = models.TextField(verbose_name='тело поста')
    image = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    view_count = models.IntegerField(default=0, verbose_name='просмотры')
    published_at = models.DateField(auto_now_add=True, verbose_name='дата публикации поста')
    creator = models.ForeignKey(User, verbose_name='создатель', on_delete=models.RESTRICT, **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
        permissions = [
            ('can_view_blog_posts', 'Can view all posts')
        ]
