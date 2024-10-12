import django_filters
from dj_rest_kit.filters import BaseFilter, BaseOrderingFilter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Transactions


class TransactionFilter(BaseFilter):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    user = django_filters.UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    subscription = django_filters.UUIDFilter(field_name="subscription__uuid", lookup_expr="exact")
    start_date = django_filters.DateFilter(field_name='creation_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='creation_date', lookup_expr='lte')

    class Meta:
        model = Transactions
        fields = ["status", "user", "subscription", "start_date", "end_date"]
