from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from .models import (
    Component,
    ComponentCategory,
    ComponentImage,
    ComponentWishlists
)
from apps.package.models import Subscription
from apps.users.serializers import UserProfileSerializer
from rest_framework import serializers
from apps.vehicle.serializers import BrandSerializer


class ComponentCategorySerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = '__all__'


class ComponentImageSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = ComponentImage
        fields = ["uuid", "image"]


class ComponentSerializer(DynamicFieldsUUIDModelSerializer):
    images = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False), write_only=True
    )
    component_images = ComponentImageSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)

    remaining_components = serializers.SerializerMethodField()

    # maker = BrandSerializer()
    # category = ComponentCategorySerializer()

    class Meta:
        model = Component
        fields = [
            'id', 'uuid', 'subscription', 'user', 'vehicle_type', 'banner', 'images', 'component_images',
            'name', 'part_number', 'maker', 'component_conditions', 'category', 'weight', 'delivery', 'is_in_stock',
            'stock_quantity', 'warranty', 'additional_guarantee_text', 'price', 'additional_description', 
            'remaining_components'
            # 'created_at',
            # 'updated_at'
        ]

    def create(self, validated_data):
        # Check for remaining vehicle
        subscription = validated_data.get("subscription")

        total_components_allowed = subscription.package.number_of_vehicle \
            if subscription.package_category == 1 else subscription.custom_package.number_of_vehicle
        vehicles_created = Component.objects.filter(subscription=subscription, is_sold=False, is_active=True, status__in=[1, 2]).count()
        remaining = total_components_allowed - vehicles_created
        if remaining <= 0:
            raise serializers.ValidationError("Number of components exceeds package limit")

        component_images = validated_data.pop('images')
        component = Component.objects.create(**validated_data)
        for media_file in component_images:
            ComponentImage.objects.create(component=component, image=media_file)
        return component

    def update(self, instance, validated_data):
        component_images = validated_data.pop('images', [])
        current_images_count = instance.component_images.count()
        # Validate number of images
        if instance.subscription:
            package = instance.subscription.package
            if len(component_images) + current_images_count > package.number_of_image:
                raise serializers.ValidationError("Number of images exceeds package limit")
            for media_file in component_images:
                ComponentImage.objects.create(vehicle=instance, image=media_file)
        return super().update(instance, validated_data)

    def get_remaining_components(self, obj):
        if obj.subscription:
            total_vehicles_allowed = obj.subscription.package.number_of_vehicle \
                if obj.subscription.package_category == 1 else obj.subscription.custom_package.number_of_vehicle
            vehicles_created = Component.objects.filter(user=obj.user, subscription=obj.subscription, is_sold=False, is_active=True, status__in=[1, 2]).count()
            return total_vehicles_allowed - vehicles_created
        return 0
    

class ComponentWishlistSerializer(DynamicFieldsUUIDModelSerializer):
    component_details = ComponentSerializer(source="component", read_only=True)

    class Meta:
        model = ComponentWishlists
        fields = [
            "uuid", "component", "user", "component_details", "created", "response_message"
        ]
