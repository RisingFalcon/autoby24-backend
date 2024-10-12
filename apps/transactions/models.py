from django.db import models
from dj_rest_kit.models import BaseUUIDModel
from apps.package.models import Subscription
from base.globals import PaymentConstants
from django.utils.translation import gettext_lazy as _


class PaymentBaseClass(BaseUUIDModel):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    tax = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=5, null=False, blank=False)
    status = models.CharField(max_length=100, null=False, blank=False)
    failure_reason = models.CharField(max_length=255, null=True, blank=True)
    internet_protocol_address = models.CharField(max_length=255, null=True, blank=True)
    internet_protocol_address_country = models.CharField(max_length=255, null=True, blank=True)
    invoice_merchant_reference = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True


class Transactions(BaseUUIDModel):
    transaction_id = models.CharField(max_length=50, null=False, blank=False)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name='subscription_transaction', null=False, blank=False
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_transaction', null=True, blank=True
    )
    status = models.CharField(choices=PaymentConstants.get_transaction_status(), null=False, blank=False, default="pending", max_length=50)
    creation_date = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Payment Trackers")
        db_table = "paymenttracker"

    def __str__(self):
        return f"{self.transaction_id}"


class Payment(PaymentBaseClass):
    transaction = models.ForeignKey(
        Transactions, on_delete=models.CASCADE, related_name='subscription_transaction', null=False, blank=False
    )
    original_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    donations = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    package_name = models.CharField(max_length=255, null=False, blank=False)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = _("Payments")
        db_table = "payment"

    def __str__(self):
        return f"{self.package_name}"


class Donation(PaymentBaseClass):
    transaction_id = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_donation', null=True, blank=True
    )
    class Meta:
        verbose_name = verbose_name_plural = _("Donations")
        db_table = "donation"

    def __str__(self):
        return f"{self.user.name}-({self.amount})"
