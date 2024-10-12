from dj_rest_kit.constants import FileFieldConstants
from dj_rest_kit.helpers import PathAndRename
from dj_rest_kit.models import BaseUUIDModel
from dj_rest_kit.validators import image_size, document_size
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Avg
from base.globals import ComponentConstants
from apps.vehicle.models import Brand
from apps.package.models import Subscription


class ComponentCategory(BaseUUIDModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = verbose_name_plural = _("Component Categories")
        db_table = "component_category"

    def __str__(self):
        return f"{self.name}"


class Component(BaseUUIDModel):
    vehicle_type = models.IntegerField(choices=ComponentConstants.get_vehicle_type_choices(), default=1)
    banner = models.ImageField(
        upload_to=PathAndRename("component-banner-image"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='component_user', null=True, blank=True
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='component_subscription',)
    name = models.CharField(max_length=255, null=False, blank=False)
    part_number = models.CharField(max_length=255, null=True, blank=True)
    maker = models.ForeignKey(Brand, on_delete=models.CASCADE)
    component_conditions = models.IntegerField(choices=ComponentConstants.get_component_condition_choices(), default=1)
    category = models.ForeignKey(ComponentCategory, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery = models.IntegerField(choices=ComponentConstants.get_delivery_choices(), default=1)
    is_in_stock = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=1)
    warranty = models.IntegerField(choices=ComponentConstants.get_warranty_type(), default=1)
    additional_guarantee_text = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    additional_description = models.TextField(null=True, blank=True)

    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(choices=ComponentConstants.get_component_status_choices(), default=2)
    activation_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = _("Components")
        db_table = "component"

    def __str__(self):
        return f"{self.name}"


class ComponentImage(BaseUUIDModel):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="component_images")
    image = models.ImageField(
        upload_to=PathAndRename("component-images"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )

    class Meta:
        verbose_name = verbose_name_plural = _("Component Images")
        db_table = "component_images"

    def __str__(self):
        return f"{self.component.name}"


class ComponentWishlists(BaseUUIDModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='wishlist_component_user')
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='wishlist_component')
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = verbose_name_plural = _("Component Wishlist")
        db_table = "component_wishlist"

    def __str__(self):
        username = self.user.first_name if self.user.first_name else self.user.email
        return f"{self.component.name} has been wishlisted by {username}"

    @property
    def response_message(self):
        return f"{self.component.name}"
