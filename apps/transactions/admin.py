from django.contrib import admin
from django.contrib.admin import register

from .models import (
    Payment,
    Transactions,
    Donation
)
# Register your models here.


admin.site.register(Payment)
admin.site.register(Transactions)
admin.site.register(Donation)
