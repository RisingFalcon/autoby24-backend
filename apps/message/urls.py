# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('messages-send/', views.SendMessageView.as_view(), name='send_message'),
    path('messages-list/', views.AdminMessageListView.as_view(), name='admin_message_list'),
    path('user-messages-list/', views.UserMessageListView.as_view(), name='user_message_list'),
    path('<uuid:uuid>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('<uuid:uuid>/update-status/', views.UpdateMessageStatusView.as_view(), name='update_message_status'),
    path('admin/send/', views.AdminSendMessageView.as_view(), name='admin_send_message'),
]