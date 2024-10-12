from dj_rest_kit.admin import BaseAdmin
from django.contrib import admin
from django.contrib.admin import register

from apps.package import models


@register(models.Package)
class PackageAdmin(BaseAdmin):
    list_display = ["name", "user_type", "package_for", "package_type", "is_active", "is_top_listing_enabled", "is_personalized_banner_enabled"]


@register(models.Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = ["user", "package", "is_expired"]


@register(models.Advertisement)
class AdvertisementAdmin(BaseAdmin):
    list_display = ["title", "link", "is_active"]


@register(models.CustomPackage)
class CustomPackageAdmin(BaseAdmin):
    list_display = ["package_type", "user", "name", "validity", "number_of_vehicle", "number_of_image", "status"]


admin.site.register(models.AdvertisementImage)
