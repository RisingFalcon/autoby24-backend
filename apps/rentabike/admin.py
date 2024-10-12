from django.contrib import admin

# Register your models here.
from .models import BikeRental, BikeImage
model_lst = [BikeRental, BikeImage]
admin.site.register(model_lst)