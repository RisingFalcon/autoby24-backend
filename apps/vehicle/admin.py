from dj_rest_kit.admin import BaseAdmin
from django.contrib import admin
from django.contrib.admin import register

from apps.vehicle import models


admin.site.register(models.VehicleImage)
admin.site.register(models.VehicleTypeNumber)
admin.site.register(models.VehicleWishlists)
admin.site.register(models.Rating)


@register(models.Vehicle)
class VehicleAdmin(BaseAdmin):
    list_display = ["brand", "model", "body_type", "is_verify"]
    # TODO: commenting for future use
    # list_filter = ["brand", "model", "body_type", "body_color", "price", "is_verify"]
    # search_fields = ["brand", "model", "body_type", "body_color", "price", "is_verify"]

@register(models.BodyType)
class BodyTypeAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]


@register(models.Brand)
class BrandAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]


@register(models.Model)
class ModelAdmin(BaseAdmin):
    list_display = ["name", "brand"]


@register(models.Colour)
class ColorAdmin(BaseAdmin):
    list_display = ["name", "code", "vehicle_type"]
