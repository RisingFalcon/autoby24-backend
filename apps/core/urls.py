from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("country", views.CountryViewSet, basename="country")
router.register("state", views.StateViewSet, basename="state")
router.register("city", views.CityViewSet, basename="city")


urlpatterns = [
    path("core/", include(router.urls)),
    path("account/", include("apps.users.urls")),
    path("vehicle/", include("apps.vehicle.urls")),
    path("package/", include("apps.package.urls")),
    path("notification/", include("apps.notification.urls")),
    path("transactions/", include("apps.transactions.urls")),
    path("rentacar/", include("apps.rentacar.urls")),
    path("features/", include("apps.features.urls")),
    path("rentagarage/", include("apps.rentagarage.urls")),
    path("rentabike/", include("apps.rentabike.urls")),
    path("component/", include("apps.component.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("messages/", include("apps.message.urls")),
]
