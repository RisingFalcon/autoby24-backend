from django.contrib import admin
from dj_rest_kit.admin import BaseAdmin
from .models import (
    MultimediaFeature,
    OptionalFeature,
    StandardFeature,
    SafetyAssistanceFeature
)

@admin.register(MultimediaFeature)
class MultimediaFeatureAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]
    # list_filter = ("name", )


@admin.register(OptionalFeature)
class OptionalFeatureAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]
    # list_filter = ("name", )


@admin.register(StandardFeature)
class StandardFeatureAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]
    # list_filter = ("name", )


@admin.register(SafetyAssistanceFeature)
class SafetyAssistanceFeatureAdmin(BaseAdmin):
    list_display = ["name", "vehicle_type"]
    # list_filter = ("name", )
