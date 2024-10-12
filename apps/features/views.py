from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from dj_rest_kit.views import BaseUUIDViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import json
from .models import (
    MultimediaFeature,
    OptionalFeature,
    StandardFeature,
    SafetyAssistanceFeature
)

from .serializers import (
    MultimediaFeatureSerializer,
    OptionalFeatureSerializer,
    StandardFeatureSerializer,
    SafetyAssistanceFeatureSerializer
)
from .filters import (
    MultimediaFeatureFilter,
    OptionalFeatureFilter,
    SafetyAssistanceFeatureFilter,
    StandardFeatureFilter
)
from .permissions import IsAdminUser
from apps.core.custom_permissions import IsAdminOrReadOnly


class MultimediaFeatureViewSet(viewsets.ModelViewSet):
    queryset = MultimediaFeature.objects.all()
    serializer_class = MultimediaFeatureSerializer
    filterset_class = MultimediaFeatureFilter
    permission_classes = [AllowAny]


class SafetyAssistanceFeatureViewSet(viewsets.ModelViewSet):
    queryset = SafetyAssistanceFeature.objects.all()
    serializer_class = SafetyAssistanceFeatureSerializer
    filterset_class = SafetyAssistanceFeatureFilter
    permission_classes = [AllowAny]


class OptionalFeatureViewSet(viewsets.ModelViewSet):
    queryset = OptionalFeature.objects.all()
    serializer_class = OptionalFeatureSerializer
    filterset_class = OptionalFeatureFilter
    permission_classes = [AllowAny]


class StandardFeatureViewSet(viewsets.ModelViewSet):
    queryset = StandardFeature.objects.all()
    serializer_class = StandardFeatureSerializer
    filterset_class = StandardFeatureFilter
    permission_classes = [AllowAny]
