from rest_framework import serializers, status
from rest_framework.response import Response
# from rest_framework import viewsets, permissions, 
from apps.vehicle.models import Brand, Model
from .models import (
    CarRental,
    CarImage,CarBrand,
    CarModel
    )

from apps.features.models import (
    MultimediaFeature,
    OptionalFeature,
    SafetyAssistanceFeature,
    StandardFeature
)

from apps.features.serializers import (
    MultimediaFeatureSerializer,
    StandardFeatureSerializer,
    SafetyAssistanceFeatureSerializer,
    OptionalFeatureSerializer
)

from apps.package.models import Subscription, Package, CustomPackage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image']

class CarRentalSerializer(serializers.ModelSerializer):
    multimedia = MultimediaFeatureSerializer(many=True)
    safety_and_assistance = SafetyAssistanceFeatureSerializer(many=True)
    standard_features = StandardFeatureSerializer(many=True)
    optional_features = OptionalFeatureSerializer(many=True)
    images = CarImageSerializer(many=True, read_only=True, source='car_image')
    image_files = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = CarRental
        fields = [
            'id', 'user', 'brand', 'model', 'running_mileage', 
            'body_type', 'registration_month', 'registration_year',
            'interior_color', 'exterior_color', 'vehicle_condition',
            'license_number', 'daily_base_price',
            'country', 'state', 'city', 'postal_code', 'street_name', 'street_number',
            'fuel_type', 'cubic_capacity', 'energy_efficiency', 'horse_power',
            'luggage_capacity', 'doors', 'seats', 'fuel_consumption', 'transmission',
            'retail_value', 'tires', 'comfort', 'multimedia', 'safety_and_assistance',
            'standard_features', 'optional_features', 'additional_field', 'status',
            'rejection_message', 'images', 'image_files','order_number',
            'pickup_date', 'pickup_time', 'return_date', 'return_time'
        ]
        read_only_fields = ['user', 'status', 'rejection_message']

    def create(self, validated_data):
        # print(f"================> {validated_data}================")
        multimedia_data = validated_data.pop('multimedia', [])
        safety_and_assistance_data = validated_data.pop('safety_and_assistance', [])
        standard_features_data = validated_data.pop('standard_features', [])
        optional_features_data = validated_data.pop('optional_features', [])
        image_files = validated_data.pop('image_files', [])
        car_rental = CarRental.objects.create(**validated_data)
        
        if multimedia_data:
            for multimedia in multimedia_data:
                multimedia_obj, created = MultimediaFeature.objects.get_or_create(**multimedia)
                car_rental.multimedia.add(multimedia_obj)
        
        if safety_and_assistance_data:
            for safety_and_assistance in safety_and_assistance_data:
                safety_obj, created = SafetyAssistanceFeature.objects.get_or_create(**safety_and_assistance)
                car_rental.safety_and_assistance.add(safety_obj)
        
        if standard_features_data:
            for standard_feature in standard_features_data:
                safety_obj, created = StandardFeature.objects.get_or_create(**standard_feature)
                car_rental.standard_features.add(safety_obj)
        
        if optional_features_data:
            for optional_feature in optional_features_data:
                safety_obj, created = OptionalFeature.objects.get_or_create(**optional_feature)
                car_rental.optional_features.add(safety_obj)
        
        if image_files:
            for image_file in image_files:
                CarImage.objects.create(car=car_rental, image=image_file)
        
        return car_rental

    def update(self, instance, validated_data):
        multimedia_data = validated_data.pop('multimedia', [])
        safety_and_assistance_data = validated_data.pop('safety_and_assistance', [])
        standard_features_data = validated_data.pop('standard_features', [])
        optional_features_data = validated_data.pop('optional_features', [])
        image_files = validated_data.pop('image_files', [])

        if multimedia_data:
            instance.multimedia.clear()
            for multimedia in multimedia_data:
                multimedia_obj, created = MultimediaFeature.objects.get_or_create(**multimedia)
                instance.multimedia.add(multimedia_obj)
        
        if safety_and_assistance_data:
            instance.safety_and_assistance.clear()
            for safety_and_assistance in safety_and_assistance_data:
                safety_obj, created = SafetyAssistanceFeature.objects.get_or_create(**safety_and_assistance)
                instance.safety_and_assistance.add(safety_obj)
        
        if standard_features_data:
            instance.standard_features.clear()
            for standard_feature in standard_features_data:
                obj, created = StandardFeature.objects.get_or_create(**standard_feature)
                instance.standard_features.add(obj)
        
        if optional_features_data:
            instance.optional_features.clear()
            for dt in optional_features_data:
                obj, created = OptionalFeature.objects.get_or_create(**dt)
                instance.optional_features.add(obj)
        
        for image_file in image_files:
            CarImage.objects.create(car=instance, image=image_file)

        return super().update(instance, validated_data)
    
    def validate(self, data):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(user=user, is_expired=False).first()
        
        if not subscription:
            raise serializers.ValidationError("You must have an active subscription to rent a car.")
        
        # vehicle check 
        max_vehicles = subscription.package.number_of_vehicle if subscription.package_category == 1 else subscription.custom_package.number_of_vehicle
        current_vehicle_count = CarRental.objects.filter(user=user).count()
        print(f"max vehicle from package => {max_vehicles} and current added vehicles => {current_vehicle_count}")
        
        if current_vehicle_count >= max_vehicles:
            raise serializers.ValidationError({"error": f"You can create a maximum of {max_vehicles} Rent-a-Car entries."})
        
        # image check 
        max_images = subscription.package.number_of_image if subscription.package_category == 1 else subscription.custom_package.number_of_image
        if len(self.context['request'].FILES.getlist('image_files')) > max_images:
            raise serializers.ValidationError({"error": f"You can upload a maximum of {max_images} images."})
        
        return data


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'name']

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name']

class CarRentalSearchSerializer(serializers.ModelSerializer):
    brand = CarBrandSerializer(read_only=True)
    model = CarModelSerializer(read_only=True)
    user_id = serializers.UUIDField(source='user.id', read_only=True)

    class Meta:
        model = CarRental
        fields = [
            'id', 'brand', 'model', 'running_mileage', 'body_type', 'registration_month',
            'registration_year', 'interior_color', 'exterior_color', 'vehicle_condition',
            'license_number', 'daily_base_price', 'country', 'state', 'city',
            'fuel_type', 'cubic_capacity', 'energy_efficiency', 'horse_power',
            'luggage_capacity', 'doors', 'seats', 'fuel_consumption', 'transmission',
            'retail_value', 'tires', 'comfort', 'multimedia', 'safety_and_assistance',
            'standard_features', 'optional_features','user.id'
        ]
