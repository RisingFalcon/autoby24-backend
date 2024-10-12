import django_filters
from dj_rest_kit.filters import BaseFilter

from apps.core import models


class CountryFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="iexact")

    class Meta:
        model = models.Country
        fields = ["name", "phone_code"]

class StateFilter(BaseFilter):
    country = django_filters.CharFilter(field_name="country__name", lookup_expr="iexact")
    class Meta:
        model = models.State
        fields = ["country", "name"]

class CityFilter(BaseFilter):
    state = django_filters.CharFilter(field_name="state__name", lookup_expr="iexact")
    class Meta:
        model = models.City
        fields = ["state", "name"]
