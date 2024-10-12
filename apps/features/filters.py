import django_filters
from dj_rest_kit.filters import BaseFilter, BaseOrderingFilter

from .models import (
    MultimediaFeature,
    SafetyAssistanceFeature,
    StandardFeature,
    OptionalFeature
)


class MultimediaFeatureFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name="vehicle_type", lookup_expr="exact")

    class Meta:
        model = MultimediaFeature
        fields = ["name", "vehicle_type"]


class SafetyAssistanceFeatureFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name="vehicle_type", lookup_expr="exact")

    class Meta:
        model = SafetyAssistanceFeature
        fields = ["name", "vehicle_type"]


class StandardFeatureFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name="vehicle_type", lookup_expr="exact")

    class Meta:
        model = StandardFeature
        fields = ["name", "vehicle_type"]


class OptionalFeatureFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name="vehicle_type", lookup_expr="exact")

    class Meta:
        model = OptionalFeature
        fields = ["name", "vehicle_type"]
