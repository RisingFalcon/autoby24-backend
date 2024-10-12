from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BikeRentalViewSet, 
    BikeImageViewSet,
    UpdateUserBikesView,BikeRentalSearchListView,
    UserBikeListView
    )

router = DefaultRouter(trailing_slash=False)
router.register('bike-rentals', BikeRentalViewSet)
router.register('bike-images', BikeImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-bikes/', UpdateUserBikesView.as_view(), name='update-user-bikes'),
    path('bike-rentals/search/', BikeRentalSearchListView.as_view(), name='bike-rental-search'),
    path('user/bike-rentals', UserBikeListView.as_view(), name='userwise_rentabike'),

]
