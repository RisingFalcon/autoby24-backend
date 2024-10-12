from django.contrib import admin
from dj_rest_kit.admin import BaseAdmin
from django.contrib.admin import register
from .models import (
    CarRental,
    CarImage, 
    )
lst = [CarRental, CarImage]
admin.site.register(lst)

# class CarImageInline(admin.TabularInline):
#     model = CarImage
#     extra = 1
#     max_num = 12

# class CarRentalAdmin(admin.ModelAdmin):
#     inlines = [CarImageInline]
#     list_display = ('brand', 'model','license_number', 'owner', 'daily_base_price', 'status')
#     list_filter = ('brand', 'fuel_type', 'transmission', 'status')
#     search_fields = ('brand', 'model', 'license_number', 'owner__username')
#     # readonly_fields = ['rejection_message'] if self.status == 'rejected' else []

#     def get_readonly_fields(self, request, obj=None):
#         if obj and obj.status == 'rejected':
#             return ['rejection_message']
#         return []

#     actions = ['approve_posts', 'reject_posts']

#     def approve_posts(self, request, queryset):
#         queryset.update(status='approved')
#     approve_posts.short_description = "Approve selected posts"

#     def reject_posts(self, request, queryset):
#         for car in queryset:
#             car.status = 'rejected'
#             # Assume there is a way to provide rejection messages via a form or other method
#             car.rejection_message = "Your specific rejection reason here."
#             car.save()
#     reject_posts.short_description = "Reject selected posts"

# admin.site.register(CarRental, CarRentalAdmin)
# admin.site.register(MultimediaFeature)
# admin.site.register(SafetyAssistanceFeature)
# admin.site.register(StandardFeature)
# admin.site.register(OptionalFeature)


# @register(CarRental)
# class CarRentalAdmin(BaseAdmin):
#     list_display = ["running_mileage"]

# @register(MultimediaFeature)
# class MultimediaFeatureAdmin(BaseAdmin):
#     list_display = ["name"]

# @register(SafetyAssistanceFeature)
# class SafetyAssistanceFeatureAdmin(BaseAdmin):
#     list_display = ["name"]

# @register(StandardFeature)
# class StandardFeatureAdmin(BaseAdmin):
#     list_display = ["name"]

# @register(OptionalFeature)
# class OptionalFeatureAdmin(BaseAdmin):
#     list_display = ["name"]

