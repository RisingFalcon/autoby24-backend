from dj_rest_kit.constants import FileFieldConstants
from dj_rest_kit.helpers import PathAndRename
from dj_rest_kit.models import BaseUUIDModel
from dj_rest_kit.validators import image_size, document_size
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Avg
from base.globals import VehicleConstants
from apps.features.models import (
    MultimediaFeature,
    OptionalFeature,
    SafetyAssistanceFeature,
    StandardFeature
)


class Brand(BaseUUIDModel):
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(
        upload_to=PathAndRename("brand-logos"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Brands")
        db_table = "brands"

    def __str__(self):
        return f"{self.name}"
    

class Model(BaseUUIDModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_models")
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=PathAndRename("model-image"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Models")
        db_table = "models"

    def __str__(self):
        return f"{self.name}"


class BodyType(BaseUUIDModel):
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Body Types")
        db_table = "body_types"

    def __str__(self):
        return f"{self.name}"


class Colour(BaseUUIDModel):
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Colors")
        db_table = "colors"
        unique_together = ('name', 'vehicle_type')

    def __str__(self):
        return f"{self.name}"


class VehicleTypeNumber(BaseUUIDModel):
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, blank=True)
    chasis_number = models.CharField(max_length=100, null=True, blank=True)
    # TODO: commented some fields to future in use.
    # country = models.ForeignKey(max_length=3000, null=True, blank=True)
    # placing_status = models.CharField(max_length=1000, null=True, blank=True)
    # out_of_traffic_since_year = models.IntegerField(default=0, null=True, blank=True)
    no_of_seats = models.IntegerField(default=0, null=True, blank=True)
    # performance = models.CharField(max_length=1000, null=True, blank=True)
    cylinder = models.IntegerField(default=0, null=True, blank=True)
    fuel_type = models.IntegerField(choices=VehicleConstants.get_fuel_type_choices(), null=True, blank=True)
    safety_rating = models.IntegerField(default=0, null=True, blank=True)
    type_number = models.CharField(max_length=100, null=True, blank=True)
    # type_of_car = models.CharField(max_length=100)
    # approval_number = models.IntegerField(default=0, null=True, blank=True)
    first_registration_year = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Vehicle type number")
        db_table = "vehicle_type_number"

    def __str__(self):
        return f"{self.type_number}"
    
    @property
    def response_message(self):
        return f"{self.type_number}"
    

class Vehicle(BaseUUIDModel):
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_vehicles', null=True, blank=True
    )
    subscription = models.ForeignKey(
        'package.Subscription', on_delete=models.CASCADE, related_name='subscription_vehicles', null=True, blank=True
    )
    vehicle_type = models.IntegerField(choices=VehicleConstants.get_vehicle_type_choices(), null=True, blank=True)
    listing_type = models.IntegerField(choices=VehicleConstants.get_vehicle_listing_type_choices(), default=2)
    banner = models.ImageField(
        upload_to=PathAndRename("vehicle-banner-image"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_vehicles", null=True, blank=True)
    year_of_registration = models.IntegerField(null=False, blank=False)
    month_of_registration = models.IntegerField(null=False, blank=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="model_vehicles", null=False, blank=False)
    is_from_mfk = models.BooleanField(default=0)
    last_mfk_inspection_year = models.IntegerField(default=0)
    last_mfk_inspection_month = models.IntegerField(default=0)
    type_number = models.ForeignKey(VehicleTypeNumber, on_delete=models.CASCADE, related_name="vehicle_type_number", null=True, blank=True)
    is_type_number_manual = models.BooleanField(default=0)
    interior_color = models.ForeignKey(Colour, on_delete=models.CASCADE, related_name="vehicle_interior_color", null=True, blank=True)
    exterior_color = models.ForeignKey(Colour, on_delete=models.CASCADE, related_name="vehicle_exterior_color", null=True, blank=True)
    running_mileage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE, related_name="body_type_vehicles", null=True, blank=True)
    transmission = models.IntegerField(choices=VehicleConstants.get_transmission_choices(), null=True, blank=True)
    vehicle_condition = models.IntegerField(choices=VehicleConstants.get_condition_choices(), null=True, blank=True)
    chasis_number = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    fuel_type = models.IntegerField(choices=VehicleConstants.get_fuel_type_choices(), null=True, blank=True)
    cubic_capacity = models.IntegerField(default=0)
    doors = models.IntegerField(default=0)
    energy_efficiency = models.TextField(null=True, blank=True)
    fuel_consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    horsepower = models.IntegerField(default=0)
    cylinders = models.IntegerField(default=0)
    kerb_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vehicle_total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gear_available = models.IntegerField(default=0)
    addition_information = models.TextField(null=True, blank=True)
    vehicle_rc = models.ImageField(
        upload_to=PathAndRename("vehicle-rc"),
        null=True, blank=True,
        validators=[FileExtensionValidator(FileFieldConstants.ATTACHMENT_FORMATS), document_size],
    )
    warranty_type = models.IntegerField(choices=VehicleConstants.get_warranty_type(), null=True, blank=True)
    additional_guarantee_text = models.CharField(null=True, blank=True, max_length=250)
    is_leasing = models.BooleanField(default=0)
    leasing_text = models.CharField(max_length=100, null=True, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    multimedia = models.ManyToManyField(MultimediaFeature, blank=True)
    safety_and_assistance = models.ManyToManyField(SafetyAssistanceFeature, blank=True)
    standard_features = models.ManyToManyField(StandardFeature, blank=True)
    optional_features = models.ManyToManyField(OptionalFeature, blank=True)

    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(choices=VehicleConstants.get_vehicle_status_choices(), default=2)
    activation_date = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Vehicles")
        db_table = "vehicles"

    def __str__(self):
        return f"{self.brand.name}"
    
    def get_average_rating(self):
        return self.rating_vehicle.aggregate(Avg('rating'))['rating__avg'] or 0.00

    def get_total_rating(self):
        return self.rating_vehicle.aggregate(Sum('rating'))['rating__sum'] or 0.00

    @property
    def response_message(self):
        return f"{self.brand.name}"


class VehicleImage(BaseUUIDModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_images")
    image = models.ImageField(
        upload_to=PathAndRename("vehicle-images"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )

    class Meta:
        verbose_name = verbose_name_plural = _("Vehicle Images")
        db_table = "vehicle_images"

    def __str__(self):
        return f"{self.vehicle.brand.name}"


class VehicleWishlists(BaseUUIDModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist_user')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='wishlist_vehicle')
    status = models.BooleanField(default=True)
    # will remove 
    class Meta:
        verbose_name = verbose_name_plural = _("Vehicle Wishlist")
        db_table = "vehicle_wishlist"

    def __str__(self):
        username = self.user.first_name if self.user.first_name else self.user.email
        return f"{self.vehicle.brand.name} has been wishlisted by {username}"

    @property
    def response_message(self):
        return f"{self.vehicle.brand.name}"
    
    
# class VehicleCustomerEnquiry(BaseUUIDModel):
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='enquiries')
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=16)
#     subject = models.CharField(max_length=50)
#     message = models.TextField()


class Rating(BaseUUIDModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='rating_user')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='rating_vehicle')
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        username = self.user.first_name if self.user.first_name else self.user.email
        return f"{username} given {self.rating} rating for {self.vehicle.brand.name}- {self.vehicle.uuid}"
    