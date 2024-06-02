import secrets
import string

from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from users.forms import UserRegisterForm, UserProfileForm, RecoveryForm, UserUpdateForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    form_class = RecoveryForm
    template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == "POST":
            user = form.cleaned_data['email']
            character = string.ascii_letters + string.digits
            password = "".join(secrets.choice(character) for i in range(12))
            user.set_password(password)
            user.save()
            send_mail(
                subject="Восстановление пароля SkyStore",
                message=f"Ваш пароль {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return HttpResponseRedirect(reverse('users:login'))
        return super().form_valid(form)


class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.can_view_all_users'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    permission_required = 'users.can_edit_is_banned'
    success_url = reverse_lazy('users:users_list')
