from django.urls import include, path
from .views import (
    PurchaseNotification,
    WelcomeNotification,
    PasswordUpdateNotification,
    SellpostApprovedNotification,
)

urlpatterns = [
    path('purchase-notification/', PurchaseNotification.as_view(), name='purchase-notification'),
    path('welcome-notification/', WelcomeNotification.as_view(), name='welcome-notification'),
    path('password-update-notification/', PasswordUpdateNotification.as_view(), name='password-update-notification'),
    path('sellpost-approved-notification/', SellpostApprovedNotification.as_view(), name='sellpost-approved-notification'),
]

