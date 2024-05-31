from django.urls import path
from django.views.decorators.cache import cache_page

from service.apps import ServiceConfig
from service.views import MainView, MessageList, MessageCreateView, MailingAttemptList, MessageUpdateView, \
    MessageDeleteView, ClientList, ClientCreateView, ClientDeleteView, ClientUpdateView, MailingList, \
    MailingCreateView, MailingDeleteView, MailingUpdateView, BlogPostList, BlogPostCreateView, BlogPostDeleteView, \
    BlogPostUpdateView, MessageDetailView, ClientDetailView, MailingDetailView, BlogPostDetailView, \
    MailingAttemptDetailView

app_name = ServiceConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('attempts/', MailingAttemptList.as_view(), name='attempts'),
    path('attempts/<int:pk>/', cache_page(60)(MailingAttemptDetailView.as_view()), name='messages_view'),

    path('messages/', cache_page(60)(MessageList.as_view()), name='messages'),
    path('messages/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='messages_view'),
    path('messages/create/', MessageCreateView.as_view(), name='messages_create'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='messages_delete'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='messages_update'),

    path('clients/', cache_page(60)(ClientList.as_view()), name='clients'),
    path('clients/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='messages_view'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='clients_update'),

    path('mailings/', cache_page(60)(MailingList.as_view()), name='mailings'),
    path('mailings/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='messages_view'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailings_create'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailings_delete'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailings_update'),

    path('blog/', cache_page(60)(BlogPostList.as_view()), name='blog'),
    path('blog/<int:pk>/', cache_page(60)(BlogPostDetailView.as_view()), name='messages_view'),
    path('blog/create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('blog/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blog_delete'),
    path('blog/update/<int:pk>/', BlogPostUpdateView.as_view(), name='blog_update')
]
