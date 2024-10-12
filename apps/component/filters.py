import django_filters
from dj_rest_kit.filters import BaseFilter, BaseOrderingFilter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.vehicle import models
from base.globals import ComponentConstants
from .models import Component, ComponentCategory


class ComponentFilter(BaseFilter):
    user = django_filters.UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    vehicle_type = django_filters.ChoiceFilter(choices=ComponentConstants.get_vehicle_type_choices())
    component_conditions = django_filters.ChoiceFilter(choices=ComponentConstants.get_component_condition_choices())
    delivery = django_filters.ChoiceFilter(choices=ComponentConstants.get_delivery_choices())
    warranty = django_filters.ChoiceFilter(choices=ComponentConstants.get_warranty_type())
    is_in_stock = django_filters.BooleanFilter()
    price = django_filters.RangeFilter()
    maker = django_filters.ModelChoiceFilter(queryset=models.Brand.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=ComponentCategory.objects.all())
    status = django_filters.NumberFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Component
        fields = [
            'vehicle_type', 
            'component_conditions', 
            'delivery', 
            'warranty', 
            'is_in_stock', 
            'price', 
            'maker', 
            'category'
        ]
