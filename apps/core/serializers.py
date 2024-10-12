from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.core import models


class StateSerializerforCountry(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.State
        fields = ["id","uuid", "name"]


class CountrySerializer(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    states = serializers.SerializerMethodField(required=False)

    class Meta:
        model = models.Country
        fields = [
            "id",
            "uuid",
            "name",
            "phone_code",
            "currency",
            "currency_symbol",
            "emoji",
            "states",
        ]

    def get_states(self, obj):
        data = obj.country_states.all()
        return StateSerializerforCountry(data, many=True).data

class StateSerializer(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.State
        fields = ["id","uuid", "country", "name"]

class CitySerializer(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.City
        fields = ["id","uuid", "state", "name"]

