from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("uuid", "email", "is_email_verify")
    list_filter = ("date_joined", "user_type")
    search_fields = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "mobile_number",
                    "whatsapp_number",
                    "user_type",
                    "profile_picture",
                    "cover_image",
                    "country",
                    "state",
                    "city",
                    "postal_code",
                    "street_number",
                    "street_name",
                    "is_email_verify",
                    "is_google_verify",
                    "is_facebook_verify",
                    "facebook_id"
                )
            },
        ),
        (
            "Dealer Info",
            {
                "fields": (
                    "dealership_name",
                    "company_registration_number",
                    "company_website",
                    "biography"
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    # "name",
                    "user_type",
                    "country",
                    "mobile_number",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ("id",)


admin.site.register(models.VerificationCode)
admin.site.register(models.DealerAvailability)
