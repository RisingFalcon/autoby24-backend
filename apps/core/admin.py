from dj_rest_kit.admin import BaseAdmin
from django.contrib.admin import register

from apps.core import models


@register(models.Country)
class CountryAdmin(BaseAdmin):
    list_display = ["name", "phone_code", "currency", "currency_symbol", "emoji"]

@register(models.State)
class CountryAdmin(BaseAdmin):
    list_display = ["country", "name", "code"]

@register(models.City)
class CountryAdmin(BaseAdmin):
    list_display = ["state", "name"]