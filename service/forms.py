from django import forms

from service.models import Message, Client, Mailing, BlogPost


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'last_name', 'first_name', 'middle_name', 'comment',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    first_sent_at = forms.DateTimeField(input_formats=['%d-%m-%Y %H:%M', '%d/%m/%Y %H:%M', '%d.%m.%Y %H:%M'])

    class Meta:
        model = Mailing
        fields = ('first_sent_at', 'frequency', 'status', 'client_list', 'message_to_send',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields["client_list"].queryset = Client.objects.filter(creator=user)
        self.fields["message_to_send"].queryset = Message.objects.filter(creator=user)


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('status',)


class BlogPostForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'image',)
