import random

from dj_rest_kit.constants import FileFieldConstants
from dj_rest_kit.helpers import PathAndRename
from dj_rest_kit.models import BaseUUIDModel, BaseModel
from dj_rest_kit.validators import image_size
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin

from apps.users import managers
from base.globals import UserConstants, UserReviewConstants



class User(AbstractBaseUser, BaseUUIDModel, PermissionsMixin, LifecycleModelMixin):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=UserConstants.get_user_type_choices(), default=2)
    # address 
    country = models.ForeignKey(
        "core.Country", on_delete=models.SET_NULL, related_name="country_users", null=True, blank=True
    )
    state = models.ForeignKey(
        "core.State", on_delete=models.SET_NULL, related_name="state_users", null=True, blank=True
    )
    city = models.ForeignKey(
        "core.City", on_delete=models.SET_NULL, related_name="city_users", null=True, blank=True
    )
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    street_number = models.CharField(max_length=50, null=True, blank=True)
    street_name = models.CharField(max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    road_number = models.CharField(max_length=50, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=PathAndRename("profile-pictures"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )
    dealership_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    company_registration_number = models.CharField(max_length=50, null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)
    is_email_verify = models.BooleanField(default=False)
    is_google_verify = models.BooleanField(default=False)
    is_facebook_verify = models.BooleanField(default=False)
    facebook_id = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(
        upload_to=PathAndRename("cover-pictures"),
        null=True, blank=True, validators=[FileExtensionValidator(FileFieldConstants.IMAGE_FORMATS), image_size],
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type", ]

    objects = managers.CustomUserManager()

    class Meta:
        verbose_name = verbose_name_plural = _("Users")
        db_table = "users"

    def __str__(self):
        return f"{self.email}"

    def get_or_create_verification_code(self):
        user_code, created = VerificationCode.objects.get_or_create(
            user=self, defaults={"code": random.randint(1000, 9999)})
        # call function generate_random_otp from base.helpers
        if not created:
            user_code.code = random.randint(1000, 9999)
            user_code.save()

        return user_code, created

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_profile_update(self):
        if self.user_type == UserConstants.PRIVATE:
            if self.first_name and self.last_name and self.mobile_number:
                return True
        elif self.user_type == UserConstants.DEALER:
            if self.dealership_name and self.address and self.company_registration_number and self.company_website:
                return True
        return False

    @property
    def response_message(self):
        return f"{self.name}"


class VerificationCode(BaseModel):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = _("Verification Code")

    def __str__(self):
        return f"Code for {self.user} is {self.code}"

class DealerAvailability(models.Model):
    dealer = models.ForeignKey(User, related_name='availability', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
    ])
    from_time = models.TimeField()
    to_time = models.TimeField()
    is_off_day = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.dealer.email} - {self.day_of_week}"


class UserReview(BaseUUIDModel):

    review_text = models.CharField(max_length=255,blank=True, null=True, default="")
    rating = models.DecimalField(max_digits=8, decimal_places=1, default=5.0)
    product_type = models.IntegerField(choices=UserReviewConstants.get_review_category_choices(), default=1)
    product_id = models.UUIDField()
    timestamp = models.DateTimeField(auto_now_add=True)
    dealer_id = models.ForeignKey(
        User,related_name='dealer_review',
        on_delete=models.CASCADE
       
    )
    client_id = models.ForeignKey(
        User,related_name='client_review',
        on_delete=models.CASCADE,
       
    )
