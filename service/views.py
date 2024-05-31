from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from service.forms import MessageForm, ClientForm, MailingForm, BlogPostForm
from service.models import MailingAttempt, Message, Mailing, Client, BlogPost


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'service/main.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        mailing_count = Mailing.objects.all().count()
        mailing_active_count = Mailing.objects.exclude(status="Завершена").count()
        client_unique = Client.objects.all().distinct().count()
        blog_random = BlogPost.objects.order_by('?')[:3]

        context_data["mailing_count"] = mailing_count
        context_data["mailing_active_count"] = mailing_active_count
        context_data["client_unique"] = client_unique
        context_data["blog_posts"] = blog_random

        return context_data


class MailingAttemptList(LoginRequiredMixin, ListView):
    model = MailingAttempt


class MailingAttemptDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempt

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = self.request.user
        if user == self.object.creator or user.is_superuser:
            return self.render_to_response(context)
        raise PermissionDenied


class MessageList(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = self.request.user
        if user == self.object.creator or user.is_superuser:
            return self.render_to_response(context)
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy('service:messages')
    form_class = MessageForm

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.creator = user
        message.save(update_fields=['creator'])
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user.is_banned:
            raise PermissionDenied
        return super().get_form_class()


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('service:messages')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return super().get_form_class()
        raise PermissionDenied


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy('service:messages')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return MessageForm
        raise PermissionDenied


class ClientList(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return self.render_to_response(context)
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    success_url = reverse_lazy('service:clients')
    form_class = ClientForm

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.creator = user
        client.save(update_fields=['creator'])
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user.is_banned:
            raise PermissionDenied
        return super().get_form_class()


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('service:clients')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return super().get_form_class()
        raise PermissionDenied


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('service:clients')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return ClientForm
        raise PermissionDenied


class MailingList(LoginRequiredMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = self.request.user
        if (user == self.object.creator or user.is_superuser or user.has_perm(
                'can_view_all_mailings')) and not user.is_banned:
            return self.render_to_response(context)
        raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    success_url = reverse_lazy('service:mailings')
    form_class = MailingForm

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.creator = user
        mailing.save(update_fields=['creator'])
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user.is_banned:
            raise PermissionDenied
        return super().get_form_class()


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('service:mailings')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser) and not user.is_banned:
            return super().get_form_class()
        raise PermissionDenied


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy('service:mailings')

    def get_form_class(self):
        user = self.request.user
        if user == (self.object.creator or user.is_superuser) and not user.is_banned:
            return MailingForm
        if user.has_perm('service.can_change_status'):
            return MailingForm
        raise PermissionDenied


class BlogPostList(LoginRequiredMixin, ListView):
    model = BlogPost


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        user = self.request.user
        if (user == self.object.creator or user.is_superuser or user.has_perm(
                'can_view_blog_posts')) and not user.is_banned:
            return self.render_to_response(context)
        raise PermissionDenied


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    success_url = reverse_lazy('service:blog')
    form_class = BlogPostForm

    def form_valid(self, form):
        blog_post = form.save()
        user = self.request.user
        blog_post.creator = user
        blog_post.save(update_fields=['creator'])
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user.is_banned:
            raise PermissionDenied
        return super().get_form_class()


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('service:blog')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser or user.has_perm(
                'can_delite_BlogPost')) and not user.is_banned:
            return super().get_form_class()
        raise PermissionDenied


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    success_url = reverse_lazy('service:blog')

    def get_form_class(self):
        user = self.request.user
        if (user == self.object.creator or user.is_superuser or user.has_perm(
                'can_edit_BlogPost')) and not user.is_banned:
            return BlogPostForm
        raise PermissionDenied
