from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ComponentCategoryViewSet,
    ComponentViewSet,
    ComponentWishlistViewSet
)


router = DefaultRouter(trailing_slash=False)
router.register("components", ComponentViewSet, basename="components")
router.register("component-category", ComponentCategoryViewSet, basename="component-category")
router.register("wishlist", ComponentWishlistViewSet, basename="wishlist")

urlpatterns = [
    path("", include(router.urls)),
]
