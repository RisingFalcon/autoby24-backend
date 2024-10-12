from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.vehicle import views

router = DefaultRouter(trailing_slash=False)
router.register("brand", views.BrandViewSet, basename="brand")
router.register("model", views.ModelViewSet, basename="model")
router.register("body-type", views.BodyTypeViewSet, basename="body-type")
router.register("colour", views.ColourViewSet, basename="color")
router.register("vehicle", views.VehicleViewSet, basename="vehicle")
router.register("vehicle-image", views.VehicleImageView, basename="vehicle-image")
router.register("wishlist", views.VehicleWishlistViewSet, basename="wishlist")
router.register("vehicle-type-number", views.VehicleTypeNumberViewSet, basename="vehicle-type-number")
router.register("rating", views.RatingViewSet, basename="rating")

urlpatterns = [
    path("", include(router.urls)),
    path('email-seller/', views.send_email_to_user, name='send_email_to_user'),
]
