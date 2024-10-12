from dj_rest_kit.models import BaseUUIDModel
from django.db import models
from django.utils.translation import gettext_lazy as _

class Country(BaseUUIDModel):
    name = models.CharField(max_length=100)
    phone_code = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    currency_symbol = models.CharField(max_length=100)
    emoji = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'core'
        verbose_name = verbose_name_plural = _("Country")

class State(BaseUUIDModel): #province
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="country_states"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = _("State")

class City(BaseUUIDModel): 
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="state_city"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

