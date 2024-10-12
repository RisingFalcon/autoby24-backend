from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionsViewset,
    DonationViewset,
    PaymentViewset,TransactionListView
)


router = DefaultRouter(trailing_slash=False)
router.register("transactions", TransactionsViewset, basename="transactions")
router.register("donation", DonationViewset, basename="donation")
router.register("payments", PaymentViewset, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    path('transactions-list/', TransactionListView.as_view(), name='transaction-list'),
]
