from django.contrib import admin

from service.models import Client, Message, Mailing, MailingAttempt, Frequency, BlogPost


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'creator',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_sent_at', 'status', 'creator',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_success', 'last_attempt',)


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'published_at', 'creator',)
