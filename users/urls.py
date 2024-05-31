from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, UserPasswordResetView, UserList, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserList.as_view(), name='users_list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset')
]
