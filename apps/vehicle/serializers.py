from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from rest_framework import serializers

from apps.vehicle import models
from apps.package.models import Subscription
from apps.users.serializers import UserProfileSerializer
from apps.features.serializers import (
    SafetyAssistanceFeatureSerializer,
    StandardFeatureSerializer,
    OptionalFeatureSerializer,
    MultimediaFeatureSerializer
)

from apps.features.models import (
    SafetyAssistanceFeature,
    StandardFeature,
    OptionalFeature,
    MultimediaFeature
)


class BrandSerializer(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Brand
        fields = [
            "id","uuid", "vehicle_type", "name", "logo", "is_active", "created", "modified",
        ]


class ModelSerializer(DynamicFieldsUUIDModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Model
        fields = [
            "id","uuid", "brand", "name", "image", "is_active", "created", "modified",
        ]


class BodyTypeSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.BodyType
        fields = [
            "uuid", "name", "vehicle_type", "is_active", "created", "modified", ]


class BodyColourSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.Colour
        fields = [
            "uuid", "name", "code", "vehicle_type", "is_active", "created", "modified",
        ]


class VehicleImageSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.VehicleImage
        fields = ["uuid", "image"]


class VehicleTypeNumberSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.VehicleTypeNumber
        fields = "__all__"


class RatingSerializer(DynamicFieldsUUIDModelSerializer):
    """Vehicle rating serializer"""
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = models.Rating
        fields = "__all__"

    def validate(self, data):
        if not data.get("vehicle"):
            raise serializers.ValidationError("Vehicle is missing.")
        return data


class VehicleSerializer(DynamicFieldsUUIDModelSerializer):

    multimedia = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    safety_and_assistance = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    standard_features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    optional_features = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    vehicle_images = VehicleImageSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False), write_only=True
    )
    body_type_name = serializers.CharField(source="body_type.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    model_name = serializers.CharField(source="model.name", read_only=True)
    remaining_vehicles = serializers.SerializerMethodField()
    package_category = serializers.SerializerMethodField()
    wishlist_details = serializers.SerializerMethodField()

    multimedia_data = MultimediaFeatureSerializer(many=True, read_only=True, source="multimedia")
    safety_and_assistance_data = SafetyAssistanceFeatureSerializer(many=True, read_only=True, source="safety_and_assistance")
    standard_features_data = StandardFeatureSerializer(many=True, read_only=True, source="standard_features")
    optional_features_data = OptionalFeatureSerializer(many=True, read_only=True, source="optional_features")
    user = UserProfileSerializer(read_only=True)

    fuel_type_display = serializers.SerializerMethodField()
    transmission_display = serializers.SerializerMethodField()
    vehicle_condition_display = serializers.SerializerMethodField()
    warranty_type_display = serializers.SerializerMethodField()
    listing_type_display = serializers.SerializerMethodField()

    average_rating = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    ratings_and_reviews = RatingSerializer(many=True, source='rating_vehicle', read_only=True)


    class Meta:
        model = models.Vehicle
        fields = ['id', 'created', 'modified', 'uuid', 'user', 'subscription', 'brand', 'vehicle_type', 'listing_type', 'listing_type_display',
                  'year_of_registration', 'month_of_registration', 'model', 'is_from_mfk', 'last_mfk_inspection_year', 
                  'last_mfk_inspection_month', 'type_number', 'is_type_number_manual', 'interior_color', 
                  'exterior_color', 'running_mileage', 'body_type', 'transmission', 'transmission_display', 'vehicle_condition', 
                  'vehicle_condition_display', 'chasis_number', 'price', 'fuel_type', 'fuel_type_display', 'cubic_capacity', 
                  'doors', 'energy_efficiency', 'fuel_consumption', 'horsepower', 'cylinders', 'kerb_weight', 'vehicle_total_weight', 
                  'gear_available', 'addition_information', 'vehicle_rc', 'warranty_type', 'warranty_type_display', 'additional_guarantee_text', 
                  'images', 'body_type_name', 'package_category', 'model_name', 'wishlist_details', 'vehicle_images', 'banner',
                  "multimedia", "safety_and_assistance", "standard_features", "optional_features", 'distance', 'average_rating', 'total_rating',
                  'ratings_and_reviews', 'multimedia_data', 'safety_and_assistance_data', 'standard_features_data', 'optional_features_data',
                  'remaining_vehicles', 'brand_name', 'is_leasing', 'leasing_text', 'is_sold', 'is_featured', 'is_verify', 
                  'is_active', 'status', 'activation_date']
        
    def get_listing_type_display(self, obj):
        return obj.get_listing_type_display() if obj.listing_type else None
    
    def get_fuel_type_display(self, obj):
        return obj.get_fuel_type_display()
    
    def get_transmission_display(self, obj):
        return obj.get_transmission_display()
    
    def get_vehicle_condition_display(self, obj):
        return obj.get_vehicle_condition_display()
    
    def get_warranty_type_display(self, obj):
        return obj.get_warranty_type_display()
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_total_rating(self, obj):
        return obj.get_total_rating()

    def get_package_category(self, obj):
        return obj.subscription.package_category if obj.subscription else 1

    def manage_type_number(self, data):
        is_type_number_manual = self.context.get('request').data.get("is_type_number_manual")
        if is_type_number_manual:
            manual_type_number = self.context.get('request').data.get("type_number_manual")
            if not models.VehicleTypeNumber.objects.filter(type_number=manual_type_number).exists():
                new_type_number = models.VehicleTypeNumber.objects.create(model=data.get("model"), brand=data.get("brand"), type_number=manual_type_number)
                data["type_number"] = new_type_number
        return data


    def validate(self, data):
        data = self.manage_type_number(data=data)

        if not self.partial:
            if not data.get("brand"):
                raise serializers.ValidationError("Missing brand name.")
            if not data.get("year_of_registration"):
                raise serializers.ValidationError("Missing registration year.")
            if not data.get("month_of_registration"):
                raise serializers.ValidationError("Missing registration month.")
            if not data.get("model"):
                raise serializers.ValidationError("Missing model name.")
            if not data.get("interior_color"):
                raise serializers.ValidationError("Missing interior color.")
            if data.get("vehicle_type") == 1 and not data.get("exterior_color"):
                raise serializers.ValidationError("Missing exterior color.")
            if not data.get("running_mileage"):
                raise serializers.ValidationError("Missing running mileage.")
            if not data.get("body_type"):
                raise serializers.ValidationError("Missing body type.")
            if data.get("vehicle_type") == 1 and not data.get("transmission"):
                raise serializers.ValidationError("Missing transmission.")
            if not data.get("vehicle_condition"):
                raise serializers.ValidationError("Missing vehicle condition.")
            if not data.get("price"):
                raise serializers.ValidationError("Missing price.")
            if not data.get("fuel_type"):
                raise serializers.ValidationError("Missing fuel type.")
            if not data.get("vehicle_type"):
                raise serializers.ValidationError("Missing Vehicle type.")

            subscription_uuid = data.get('subscription')
            if subscription_uuid:
                required_no_of_image = subscription_uuid.package.number_of_image \
                    if subscription_uuid.package_category == 1 else subscription_uuid.custom_package.number_of_image
                required_no_of_vehicle = subscription_uuid.package.number_of_vehicle \
                    if subscription_uuid.package_category == 1 else subscription_uuid.custom_package.number_of_vehicle

                vehicle_images = data.get('images', [])
                if len(vehicle_images) > required_no_of_image:
                    raise serializers.ValidationError("Number of images exceeds package limit")
                if required_no_of_vehicle is not None and models.Vehicle.objects.filter(
                        subscription=subscription_uuid, is_sold=False).count() >= required_no_of_vehicle:
                    raise serializers.ValidationError("Number of vehicles exceeds package limit")
        return data

    def get_wishlist_details(self, obj) -> dict:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            wishlists = obj.wishlist_vehicle.filter(user=request.user).first()
            if wishlists:
                return {
                    "uuid": wishlists.uuid,
                    "is_wishlisted": True,
                }
        return {
            "is_wishlisted": False,
        }
        
    def get_remaining_vehicles(self, obj):
        if obj.subscription:
            total_vehicles_allowed = obj.subscription.package.number_of_vehicle \
                if obj.subscription.package_category == 1 else obj.subscription.custom_package.number_of_vehicle
            vehicles_created = models.Vehicle.objects.filter(user=obj.user, subscription=obj.subscription, is_sold=False, is_active=True, status__in=[1, 2]).count()
            return total_vehicles_allowed - vehicles_created
        return 0

    def create(self, validated_data):
        vehicle_images = validated_data.pop('images')
        multimedia_data = validated_data.pop('multimedia', [])
        safety_and_assistance_data = validated_data.pop('safety_and_assistance', [])
        standard_features_data = validated_data.pop('standard_features', [])
        optional_features_data = validated_data.pop('optional_features', [])

        vehicle = models.Vehicle.objects.create(**validated_data)

        for media_file in vehicle_images:
            models.VehicleImage.objects.create(vehicle=vehicle, image=media_file)
        
        if multimedia_data:
            multimedia_data = eval(multimedia_data[0])

            for multimedia in multimedia_data:
                try:
                    multimedia_obj, created = MultimediaFeature.objects.get_or_create({"uuid": multimedia})
                    vehicle.multimedia.add(multimedia_obj)
                except MultimediaFeature.MultipleObjectsReturned as err:
                    multimedia_obj = MultimediaFeature.objects.filter(uuid=multimedia).first()
                    vehicle.multimedia.add(multimedia_obj)
                except Exception as err:
                    pass
        
        if safety_and_assistance_data:
            safety_and_assistance_data = eval(safety_and_assistance_data[0])
            for safety_and_assistance in safety_and_assistance_data:
                try:
                    safety_obj, created = SafetyAssistanceFeature.objects.get_or_create({"uuid": safety_and_assistance})
                    vehicle.safety_and_assistance.add(safety_obj)
                except SafetyAssistanceFeature.MultipleObjectsReturned as err:
                    safety_obj = SafetyAssistanceFeature.objects.filter(uuid=safety_and_assistance).first()
                    vehicle.safety_and_assistance.add(safety_obj)
                except Exception as err:
                    pass
        
        if standard_features_data:
            standard_features_data = eval(standard_features_data[0])
            for standard_feature in standard_features_data:
                try:
                    standard_obj, created = StandardFeature.objects.get_or_create({"uuid": standard_feature})
                    vehicle.standard_features.add(standard_obj)
                except StandardFeature.MultipleObjectsReturned as err:
                    standard_obj = StandardFeature.objects.filter(uuid=standard_feature).first()
                    vehicle.standard_features.add(standard_obj)
                except Exception as err:
                    pass
        
        if optional_features_data:
            optional_features_data = eval(optional_features_data[0])
            for optional_feature in optional_features_data:
                try:
                    optional_obj, created = OptionalFeature.objects.get_or_create({"uuid": optional_feature})
                    vehicle.optional_features.add(optional_obj)
                except OptionalFeature.MultipleObjectsReturned as err:
                    optional_obj = OptionalFeature.objects.filter(uuid=optional_feature).first()
                    vehicle.optional_features.add(optional_obj)
                except Exception as err:
                    pass

        return vehicle

    def update(self, instance, validated_data):
        vehicle_images = validated_data.pop('images', [])
        current_images_count = instance.vehicle_images.count()

        multimedia_data = validated_data.pop('multimedia', [])
        safety_and_assistance_data = validated_data.pop('safety_and_assistance', [])
        standard_features_data = validated_data.pop('standard_features', [])
        optional_features_data = validated_data.pop('optional_features', [])

        # Validate number of images
        if instance.subscription:
            package = instance.subscription.package
            if len(vehicle_images) + current_images_count > package.number_of_image:
                raise serializers.ValidationError("Number of images exceeds package limit")

            for media_file in vehicle_images:
                models.VehicleImage.objects.create(vehicle=instance, image=media_file)
        requesst_data = dict(self.context.get('request').data)

        if "multimedia" in requesst_data:
            instance.multimedia.clear()
        if "safety_and_assistance" in requesst_data:
            instance.safety_and_assistance.clear()
        if "standard_features" in requesst_data:
            instance.standard_features.clear()
        if "optional_features" in requesst_data:
            instance.optional_features.clear()

        if multimedia_data:
            multimedia_data = eval(multimedia_data[0])
            if len(multimedia_data):
                instance.multimedia.clear()
            for multimedia in multimedia_data:
                multimedia_obj, created = MultimediaFeature.objects.get_or_create(**multimedia)
                instance.multimedia.add(multimedia_obj)
        
        if safety_and_assistance_data:
            safety_and_assistance_data = eval(safety_and_assistance_data[0])
            if len(safety_and_assistance_data):
                instance.safety_and_assistance.clear()
            for safety_and_assistance in safety_and_assistance_data:
                safety_obj, created = SafetyAssistanceFeature.objects.get_or_create(**safety_and_assistance)
                instance.safety_and_assistance.add(safety_obj)
        
        if standard_features_data:
            standard_features_data = eval(standard_features_data[0])
            if len(standard_features_data):
                instance.standard_features.clear()
            for standard_feature in standard_features_data:
                safety_obj, created = StandardFeature.objects.get_or_create(**standard_feature)
                instance.standard_features.add(safety_obj)
        
        if optional_features_data:
            optional_features_data = eval(optional_features_data[0])
            if len(optional_features_data):
                instance.optional_features.clear()
            for optional_feature in optional_features_data:
                safety_obj, created = OptionalFeature.objects.get_or_create(**optional_feature)
                instance.optional_features.add(safety_obj)

        return super().update(instance, validated_data)


class VehicleWishlistSerializer(DynamicFieldsUUIDModelSerializer):
    vehicle_details = VehicleSerializer(source="vehicle", read_only=True)

    class Meta:
        model = models.VehicleWishlists
        fields = [
            "uuid", "vehicle", "user", "vehicle_details", "created", "response_message"
        ]


# class VehicleCustomerEnquirySerializer(DynamicFieldsUUIDModelSerializer):
#     class Meta:
#         model = models.VehicleCustomerEnquiry
#         fields = '__all__'
