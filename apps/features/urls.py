# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MultimediaFeatureViewSet,
    OptionalFeatureViewSet,
    StandardFeatureViewSet,
    SafetyAssistanceFeatureViewSet
)


router = DefaultRouter()
router.register(r'multimedia', MultimediaFeatureViewSet)
router.register(r'optional', OptionalFeatureViewSet)
router.register(r'safety', SafetyAssistanceFeatureViewSet)
router.register(r'standard', StandardFeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
