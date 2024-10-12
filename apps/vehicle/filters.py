import django_filters
from dj_rest_kit.filters import BaseFilter, BaseOrderingFilter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.vehicle import models


class MultipleUUIDFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Custom filter for handling multiple UUIDs.
    """
    def filter(self, qs, value):
        if not value:
            return qs

        # Exclude records with null values
        qs = qs.exclude(**{f"{self.field_name}__isnull": True})

        # Split the input value by commas, remove whitespace, and validate each UUID
        try:
            uuids = [eval(uuid.strip()) for uuid in value if uuid]
        except Exception as e:
            raise ValidationError(_("Enter a valid UUID list."))

        # Apply the filter
        return qs.filter(**{f"{self.field_name}__in": uuids})


class BrandFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:
        model = models.Brand
        fields = ["name", "is_active", "vehicle_type"]


class ModelFilter(BaseFilter):
    brand = django_filters.UUIDFilter(field_name="brand__uuid", lookup_expr="exact")
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name="brand__vehicle_type", lookup_expr="exact")

    class Meta:
        model = models.Model
        fields = ["brand", "name", "is_active", "vehicle_type"]


class BodyTypeFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:
        model = models.BodyType
        fields = ["name", "is_active", "vehicle_type"]


class BodyColourFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:
        model = models.Colour
        fields = ["name", "is_active", "vehicle_type"]


class VehicleTypeFilter(BaseFilter):
    type_number = django_filters.CharFilter(field_name="type_number", lookup_expr="exact")
    chasis_number = django_filters.CharFilter(field_name="chasis_number", lookup_expr="exact")
    brand = django_filters.UUIDFilter(field_name="brand__uuid", lookup_expr="exact")
    model = django_filters.UUIDFilter(field_name="model__uuid", lookup_expr="exact")

    class Meta:
        model = models.VehicleTypeNumber
        fields = ["type_number", "brand", "vehicle_type", "chasis_number", "model"]


class VehicleFilter(BaseFilter):
    user = django_filters.UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    package = django_filters.UUIDFilter(field_name="subscription__package__uuid", lookup_expr="exact")

    exterior_color = MultipleUUIDFilter(field_name="exterior_color__uuid")
    interior_color = MultipleUUIDFilter(field_name="interior_color__uuid")
    multimedia = MultipleUUIDFilter(field_name='multimedia__uuid')
    optional_features = MultipleUUIDFilter(field_name='optional_features__uuid')
    safety_and_assistance = MultipleUUIDFilter(field_name='safety_and_assistance__uuid')
    standard_features = MultipleUUIDFilter(field_name='standard_features__uuid')
    body_type = MultipleUUIDFilter(field_name='body_type__uuid')
    vehicle_condition = MultipleUUIDFilter(field_name='vehicle_condition')
    transmission = MultipleUUIDFilter(field_name='transmission')
    energy_efficiency = MultipleUUIDFilter(field_name='energy_efficiency')
    doors = MultipleUUIDFilter(field_name='doors')

    brand = django_filters.UUIDFilter(field_name="brand__uuid", lookup_expr="exact")
    model = django_filters.UUIDFilter(field_name="model__uuid", lookup_expr="exact")
    package_type = django_filters.NumberFilter(field_name="subscription__package__package_type", lookup_expr="exact")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_distance = django_filters.NumberFilter(field_name="distance", lookup_expr="gte")
    max_distance = django_filters.NumberFilter(field_name="distance", lookup_expr="lte")

    class Meta:
        model = models.Vehicle
        fields = [
            "is_active", "is_sold", "is_featured", "month_of_registration", "year_of_registration",
            "vehicle_type", "listing_type", "horsepower", "fuel_consumption", "running_mileage",
            "fuel_type", "gear_available", "cylinders", "is_from_mfk", "last_mfk_inspection_year", 
            "last_mfk_inspection_month", "cubic_capacity", "status", "is_verify", "warranty_type",
            "fuel_consumption", "horsepower", "kerb_weight", "vehicle_total_weight", "gear_available"
        ]
        ordering = BaseOrderingFilter(
        fields=(
            ("id", "id"),
            ("price", "price"),
            ("is_active", "is_active"),
            ("is_sold", "is_sold"),
            ("is_featured", "is_featured")
        )
    )
