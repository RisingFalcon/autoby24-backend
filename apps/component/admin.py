from django.contrib import admin
from .models import (
    ComponentImage,
    Component,
    ComponentCategory
)
from dj_rest_kit.admin import BaseAdmin
from django.contrib.admin import register


@register(ComponentCategory)
class ComponentCategoryAdmin(BaseAdmin):
    list_display = ["name"]


@register(Component)
class ComponentAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type", "maker", "component_conditions", "category", "is_in_stock", "stock_quantity", "price"]


@register(ComponentImage)
class ComponentImageAdmin(BaseAdmin):
    list_display = ["component", "image"]
