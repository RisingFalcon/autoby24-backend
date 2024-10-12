import django_filters
from dj_rest_kit.filters import BaseFilter

from apps.package import models


class PackageFilter(BaseFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="exact")
    # is_expired = django_filters.BooleanFilter(field_name="package_subscriptions__is_expired")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = models.Package
        fields = ["user_type", "package_type", "package_for", "is_top_listing_enabled", "is_personalized_banner_enabled"]
        
        
class CustomPackageFilter(BaseFilter):
    user = django_filters.UUIDFilter(field_name="user", lookup_expr="exact")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    # is_expired = django_filters.BooleanFilter(field_name="package_subscriptions__is_expired")

    class Meta:
        model = models.CustomPackage
        fields = ["user", "package_type", "package_for"]


class AdvertisementFilter(BaseFilter):
    user = django_filters.UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    subscription = django_filters.UUIDFilter(field_name="subscription__uuid", lookup_expr="exact")

    class Meta:
        model = models.Advertisement
        fields = [
            "user", "is_active", "status"
        ]


class PublicAdvertisementFilter(BaseFilter):
    package_type = django_filters.NumberFilter(field_name="subscription__package__package_type", lookup_expr="exact")

    class Meta:
        model = models.Advertisement
        fields = [
            "is_active", "status"
        ]


class SubscriptionFilter(BaseFilter):
    user = django_filters.UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    package_type = django_filters.NumberFilter(field_name="package__package_type", lookup_expr="exact")
    vehicle_type = django_filters.NumberFilter(field_name='subscription_vehicles__vehicle_type', lookup_expr="exact")
    is_paid = django_filters.BooleanFilter(field_name="is_paid")
    is_activated = django_filters.BooleanFilter(field_name="is_activated")
    is_expired = django_filters.BooleanFilter(field_name="is_expired")
    package_for = django_filters.NumberFilter(field_name="package__package_for", lookup_expr="exact")
    is_top_listing_enabled = django_filters.NumberFilter(field_name="package__is_top_listing_enabled", lookup_expr="exact")
    is_personalized_banner_enabled = django_filters.NumberFilter(field_name="package__is_personalized_banner_enabled", lookup_expr="exact")

    class Meta:
        model = models.Subscription
        fields = ["user", "is_expired", "is_paid", "is_activated"]
