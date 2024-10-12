from django.db import models
from dj_rest_kit.models import BaseUUIDModel
from apps.package.models import Subscription
from base.globals import PaymentConstants
from django.utils.translation import gettext_lazy as _
from base.globals import VehicleConstants


class MultimediaFeature(BaseUUIDModel):
    name = models.CharField(max_length=50)
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def response_message(self):
        return f"{self.name}"


class SafetyAssistanceFeature(BaseUUIDModel):
    name = models.CharField(max_length=50)
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def response_message(self):
        return f"{self.name}"


class StandardFeature(BaseUUIDModel):
    name = models.CharField(max_length=50)
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def response_message(self):
        return f"{self.name}"
    

class OptionalFeature(BaseUUIDModel):
    name = models.CharField(max_length=50)
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def response_message(self):
        return f"{self.name}"
