from django.contrib import admin
from dj_rest_kit.admin import BaseAdmin
from django.contrib.admin import register
from .models import (
    GarageRental,
    RentaGarageImage
    )
lst = [GarageRental, RentaGarageImage]
admin.site.register(lst)
