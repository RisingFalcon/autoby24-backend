from dj_rest_kit.views import BaseUUIDViewSet
from rest_framework import permissions

from apps.core import filters, models, serializers


# Create your views here.
class CountryViewSet(BaseUUIDViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    filterset_class = filters.CountryFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # http_method_names = ["get"]

class StateViewSet(BaseUUIDViewSet):
    serializer_class = serializers.StateSerializer
    queryset = models.State.objects.all()
    filterset_class = filters.StateFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # http_method_names = ["get"]

class CityViewSet(BaseUUIDViewSet):
    serializer_class = serializers.CitySerializer
    queryset = models.City.objects.all()
    filterset_class = filters.CityFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
