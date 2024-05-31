from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_banned',)

class RecoveryForm(PasswordResetForm):
    pass

    def clean_email(self):
        cleaned_data = self.cleaned_data['email']
        try:
            cleaned_data = User.objects.filter(is_active=True).get(email=cleaned_data)
        except User.DoesNotExist:
            raise forms.ValidationError('Пользователя с такой почтой не существует или он не активирован')
        return cleaned_data
