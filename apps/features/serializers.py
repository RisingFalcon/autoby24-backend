# serializers.py
from rest_framework import serializers
from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from .models import (
    MultimediaFeature,
    SafetyAssistanceFeature,
    StandardFeature,
    OptionalFeature
)


class MultimediaFeatureSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = MultimediaFeature
        fields = ['id', 'uuid', 'name']

class SafetyAssistanceFeatureSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = SafetyAssistanceFeature
        fields = ['id', 'uuid', 'name']

class StandardFeatureSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = StandardFeature
        fields = ['id', 'uuid', 'name']

class OptionalFeatureSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = OptionalFeature
        fields = ['id', 'uuid', 'name']
