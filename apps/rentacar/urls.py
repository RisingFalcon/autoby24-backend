from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CarRentalViewSet, 
    CarImageViewSet,
    UpdateUserCarsView,
    CarRentalSearchListView,
    UserCarsListView
    )

router = DefaultRouter(trailing_slash=False)
router.register('car-rentals', CarRentalViewSet)
router.register('car-images', CarImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-cars/', UpdateUserCarsView.as_view(), name='update-user-cars'),
    path('user/car-rentals', UserCarsListView.as_view(), name='userwise_rentacar'),
]

urlpatterns += [
    path('car-rentals/search/', CarRentalSearchListView.as_view(), name='car-rental-search'),
]
