import django_filters
from dj_rest_kit.filters import BaseFilter

from apps.rentacar import models


# class CarModelFilter(BaseFilter):
#     brand = django_filters.CharFilter(field_name="brand__name", lookup_expr="iexact")

#     class Meta:
#         model = models.CarModel
#         fields = ["brand", "name"]

# class StateFilter(BaseFilter):
#     country = django_filters.CharFilter(field_name="country__name", lookup_expr="iexact")
#     class Meta:
#         model = models.State
#         fields = ["country", "name"]
