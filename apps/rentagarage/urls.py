from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GarageRentalViewSet, 
    GarageImageViewSet,
    UpdateUserGaragesView,GarageRentalSearchListView,
    UserGarageListView
    )

router = DefaultRouter(trailing_slash=False)
router.register('garage', GarageRentalViewSet)
router.register('images', GarageImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-garages/', UpdateUserGaragesView.as_view(), name='update-user-garages'),
    path('garage-rentals/search/', GarageRentalSearchListView.as_view(), name='garage-rental-search'),
    path('user/garage', UserGarageListView.as_view(), name='userwise_rentagarage'),
]
