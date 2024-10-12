from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("package", views.PackageViewSet, basename="package")
router.register("custom-package", views.CustomPackageViewSet, basename="custom-package")
router.register("subscription", views.SubscriptionViewSet, basename="subscription")
router.register("advertisement", views.AdvertisementViewSet, basename="advertisement")
router.register("advertisement-image", views.AdvertisementImageView, basename="advertisement-image")
router.register("public-advertisements", views.PublicAdvertisementList, basename="public_advertisements")
router.register("bookmark", views.PackageBookmarkViewSet, basename="bookmark")


urlpatterns = [
    path("", include(router.urls)),

]
