from django.db import models
from config.models import CommonModel
from django.utils.translation import gettext_lazy as _

# import 
from apps.core.models import Country, State, City
from base.globals import (
    VehicleConstants,
    RentagarageConstants
)
from apps.features.models import (
    OptionalFeature,
    StandardFeature
)    


class GarageRental(CommonModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    # garage details 
    name = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=50, choices=RentagarageConstants.get_garage_type_choices())
    garage_condition = models.TextField(null=True, blank=True)
    monthly_rent_price = models.DecimalField(max_digits=5, decimal_places=2)

    # Garage location 
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=50)
    street_name = models.CharField(max_length=200)
    street_number = models.PositiveIntegerField()

    # features 
    standard_features = models.ManyToManyField(StandardFeature)
    optional_features = models.ManyToManyField(OptionalFeature)

    additional_field = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=VehicleConstants.get_vehicle_status_choices(), default=2)
    rejection_message = models.TextField(blank=True, null=True)
    order_number = models.PositiveIntegerField(default=1000)
    pickup_date = models.DateField(blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    return_time = models.TimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} => {self.type} => {self.garage_condition}"
    
    class Meta:
        app_label = 'rentagarage'
        verbose_name = verbose_name_plural = _("GarageRental")

class RentaGarageImage(models.Model):
    renta_garage = models.ForeignKey(GarageRental, on_delete=models.CASCADE, related_name='rentagarage_images')
    image = models.ImageField(upload_to='rentagarage/')

    class Meta:
        app_label = 'rentagarage'
