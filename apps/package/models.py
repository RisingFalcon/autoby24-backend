from dj_rest_kit.constants import FileFieldConstants
from dj_rest_kit.helpers import PathAndRename
from dj_rest_kit.models import BaseUUIDModel
from dj_rest_kit.validators import image_size
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE

from base.globals import (
    PackageConstants,
    UserConstants,
    AdvertisementConstants
)


class Package(BaseUUIDModel):
    user_type = models.IntegerField(choices=UserConstants.get_user_type_choices())
    package_for = models.BigIntegerField(choices=PackageConstants.get_package_for_choices(), default=1)
    package_type = models.IntegerField(choices=PackageConstants.get_package_type_choices())
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity = models.IntegerField(default=0, help_text="In days")
    number_of_vehicle = models.IntegerField(default=0)
    number_of_image = models.IntegerField(default=0)
    extra_image_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_top_listing_enabled = models.BooleanField(default=False, help_text="Enable if you want to mark this package in top listing")
    is_personalized_banner_enabled = models.BooleanField(default=False, help_text="Enable if you want to add personalized banner image.")

    class Meta:
        verbose_name = verbose_name_plural = _("Packages")
        db_table = "packages"

    def __str__(self):
        return f"{self.name}"

    @property
    def response_message(self):
        return f"{self.name}"
    

class PackageBookMark(BaseUUIDModel):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_bookmark')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_package_bookmark')

    class Meta:
        verbose_name = verbose_name_plural = _("PackageBookmark")
        db_table = "package_bookmark"

    def __str__(self):
        return f"{self.package.name}"

    @property
    def response_message(self):
        return f"{self.package.name}"


class CustomPackage(BaseUUIDModel):
    package_for = models.BigIntegerField(choices=PackageConstants.get_package_for_choices(), default=1)
    package_type = models.IntegerField(choices=PackageConstants.get_package_type_choices())
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_custom_packages')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    validity = models.IntegerField(default=0, help_text="In days")
    number_of_vehicle = models.IntegerField(default=0)
    number_of_image = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(choices=PackageConstants.get_package_status_choices(), default=2)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status_change_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def response_message(self):
        return f"{self.name}"


class Advertisement(BaseUUIDModel):
    subscription = models.ForeignKey(
        'package.Subscription', on_delete=models.CASCADE, related_name='subscription_advertisements', null=True,
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_advertisements', null=True, blank=True
    )
    title = models.CharField(max_length=100)
    link = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(choices=AdvertisementConstants.get_advertisement_status_choices(), default=2)

    class Meta:
        verbose_name = verbose_name_plural = _("Advertisements")
        db_table = "advertisements"

    def __str__(self):
        return f"{self.title}"

    @property
    def response_message(self):
        return f"{self.title}"


class AdvertisementImage(BaseUUIDModel):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="advertisement_images")
    image = models.ImageField(
        upload_to=PathAndRename("advertisement-images"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )

    class Meta:
        verbose_name = verbose_name_plural = _("Advertisement Images")
        db_table = "advertisement_images"

    def __str__(self):
        return f"{self.advertisement.title}"


class Subscription(LifecycleModelMixin, BaseUUIDModel):
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='user_subscriptions', null=True, blank=True
    )
    package = models.ForeignKey(
        'package.Package', on_delete=models.CASCADE, related_name='package_subscriptions', null=True,
    )
    custom_package = models.ForeignKey(
        'package.CustomPackage', on_delete=models.CASCADE, related_name='custom_package_subscriptions', null=True, blank=True
    )
    package_category = models.IntegerField(choices=PackageConstants.get_package_category_choices(), default=1)
    activation_date = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)
    is_activated = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    

    class Meta:
        verbose_name = verbose_name_plural = _("Subscriptions")
        db_table = "subscriptions"

    def __str__(self):
        return f"{self.package.name}" if self.package_category == 1 else f"{self.custom_package.name}"

    @property
    def response_message(self):
        return f"{self.package.name}" if self.package_category == 1 else f"{self.custom_package.name}"

    @hook(AFTER_CREATE)
    def activate_subscription(self):
        package_validity_days = self.package.validity if self.package_category == 1 else self.custom_package.validity
        if package_validity_days > 0:
            self.expiry_date = timezone.now().date() + timezone.timedelta(days=package_validity_days)
            self.save()
