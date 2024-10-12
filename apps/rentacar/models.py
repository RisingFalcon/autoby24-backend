from django.db import models
from config.models import CommonModel
from django.utils.translation import gettext_lazy as _

# import 
from apps.core.models import Country, State, City
from apps.vehicle.models import Brand, Model
from base.globals import (
    RentacarConstants,
    VehicleConstants
)
from apps.features.models import (
    MultimediaFeature,
    OptionalFeature,
    SafetyAssistanceFeature,
    StandardFeature
)

class CarBrand(CommonModel):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    def __str__(self):
        return f"{self.name}"

class CarModel(CommonModel):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='car_models', verbose_name=_('Brand'))
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    
    def __str__(self):
        return f"{self.brand} => {self.name}"      


class CarRental(CommonModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    running_mileage = models.PositiveIntegerField()
    body_type = models.CharField(max_length=50, choices=RentacarConstants.get_body_type_choices())
    
    registration_month = models.CharField(max_length=20, choices=RentacarConstants.get_month_choices())
    registration_year = models.PositiveIntegerField()
    interior_color = models.CharField(max_length=50, null=True, blank=True)
    exterior_color = models.CharField(max_length=50, null=True, blank=True)
    vehicle_condition = models.CharField(max_length=50, choices=RentacarConstants.get_condition_choices())
    license_number = models.CharField(max_length=100, unique=True)
    daily_base_price = models.DecimalField(max_digits=5, decimal_places=2)

    # address 
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=50)
    street_name = models.CharField(max_length=200)
    street_number = models.PositiveIntegerField()

    # features 
    fuel_type = models.CharField(max_length=50, choices=RentacarConstants.get_fuel_type_choices())
    cubic_capacity = models.PositiveBigIntegerField(null=True, blank=True)
    energy_efficiency = models.CharField(max_length=5, choices=RentacarConstants.get_energy_efficiency_choices())
    horse_power = models.PositiveBigIntegerField()
    luggage_capacity = models.PositiveBigIntegerField()
    doors = models.PositiveBigIntegerField()
    seats = models.PositiveBigIntegerField()
    fuel_consumption = models.PositiveBigIntegerField()
    transmission = models.CharField(max_length=50, choices=RentacarConstants.get_transmission_choices())
    retail_value = models.PositiveIntegerField()
    tires = models.CharField(max_length=20, choices=RentacarConstants.get_tyre_choices())
    comfort = models.CharField(max_length=20, choices=RentacarConstants.get_comfort_choices())
    multimedia = models.ManyToManyField(MultimediaFeature)
    safety_and_assistance = models.ManyToManyField(SafetyAssistanceFeature)
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
        return f"{self.brand} {self.model} ({self.license_number})"
    
    class Meta:
        app_label = 'rentacar'
        verbose_name = verbose_name_plural = _("CarRental")

class CarImage(models.Model):
    car = models.ForeignKey(CarRental, on_delete=models.CASCADE, related_name='car_image')
    image = models.ImageField(upload_to='car_images/')

    class Meta:
        app_label = 'rentacar'
