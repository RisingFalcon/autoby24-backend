from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from django.utils import timezone
from rest_framework import serializers

from apps.package import models
from apps.users.serializers import UserProfileSerializer
from apps.vehicle.serializers import VehicleSerializer
from apps.component.serializers import ComponentSerializer


class PackageSerializer(DynamicFieldsUUIDModelSerializer):
    package_for_display = serializers.SerializerMethodField()
    package_type_display = serializers.SerializerMethodField()
    class Meta:
        model = models.Package
        fields = [
            "uuid", "user_type", "package_for", "package_for_display", "package_type", "package_type_display", "name", 
            "description", "price", "validity", "number_of_vehicle", "number_of_image", "is_active", "created", 
            "modified", "response_message", "is_top_listing_enabled", "is_personalized_banner_enabled", "extra_image_price"
        ]
    
    def get_package_for_display(self, obj):
        return obj.get_package_for_display()
    
    def get_package_type_display(self, obj):
        return obj.get_package_type_display()
        

class PackageBookMarkSerializer(DynamicFieldsUUIDModelSerializer):
    package_detail = PackageSerializer(source="package", read_only=True)
    user_detail = UserProfileSerializer(source="user", read_only=True)

    class Meta:
        model = models.PackageBookMark
        fields = ["id", "uuid", "user", "package", "created", "modified", "user_detail", "package_detail"]


class CustomPackageSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.CustomPackage
        fields = "__all__"
        # fields = [
        #     "uuid", "user", "name", "description",  "validity", "number_of_vehicle",
        #     "number_of_image", "response_message", "package_type", "status",
        # ]


class AdvertisementImageSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.AdvertisementImage
        fields = ["uuid", "image"]


class SubscriptionSerializer(DynamicFieldsUUIDModelSerializer):
    user_details = UserProfileSerializer(source="user", read_only=True)
    # user_details = UserProfileSerializer(source="user", read_only=True, fields=['email', 'first_name', 'last_name'])
    package_details = PackageSerializer(source="package", read_only=True)
    custom_package_details = CustomPackageSerializer(source="custom_package", read_only=True)
    remaining_vehicle = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    component_details = serializers.SerializerMethodField()
    remaining_components = serializers.SerializerMethodField()
    # is_expired = serializers.SerializerMethodField()

    class Meta:
        model = models.Subscription
        fields = [
            "uuid", "user", "user_details", "package", "custom_package", "package_category", "package_details", "vehicle_details", 
            "remaining_vehicle", "custom_package_details", "component_details",
            "remaining_components", "expiry_date", "is_expired", "is_activated", "activation_date", "is_paid", "response_message"
        ]

    # def get_is_expired(self, obj):
    #     if self.context['request'].method != "POST":
    #         if obj.expiry_date and obj.expiry_date > timezone.now().date():
    #             return False
    #         return True
    #     return False

    def get_remaining_vehicle(self, obj):
        if self.context['request'].method != "POST":
            package = obj.package if obj.package_category == 1 else obj.custom_package
            return package.number_of_vehicle - obj.subscription_vehicles.count()
        return []

    def get_vehicle_details(self, obj):
        if self.context['request'].method != "POST":
            subscription_vehicles = obj.subscription_vehicles
            data = VehicleSerializer(subscription_vehicles, many=True)
            return data.data
        return []
    
    def get_component_details(self, obj):
        if self.context['request'].method != "POST" and obj.package.package_type == 8:
            component_subscription = obj.component_subscription
            data = ComponentSerializer(component_subscription, many=True)
            return data.data
        return []
    
    def get_remaining_components(self, obj):
        if self.context['request'].method != "POST" and obj.package.package_type == 8:
            package = obj.package if obj.package_category == 1 else obj.custom_package
            return package.number_of_vehicle - obj.component_subscription.count()
        return 0


class AdvertisementSerializer(DynamicFieldsUUIDModelSerializer):
    advertisement_images = AdvertisementImageSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False), write_only=True
    )
    subscription_details = SubscriptionSerializer(source="subscription", read_only=True)
    active_date = serializers.SerializerMethodField(read_only=True)
    expiry_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Advertisement
        fields = [
            "uuid", "subscription", "subscription_details", "user", "title", "link", "is_active", "images",
            "advertisement_images", "active_date", "expiry_date", "response_message", "status"
        ]

    def validate(self, data):
        subscription = data.get('subscription')
        if subscription:
            package = subscription.package if subscription.package_category == 1 else subscription.custom_package
            vehicle_images = data.get('images', [])
            if len(vehicle_images) > package.number_of_image:
                raise serializers.ValidationError("Number of images exceeds package limit")
        return data

    def create(self, validated_data):
        advertisement_images = validated_data.pop('images')

        advertisement = models.Advertisement.objects.create(**validated_data)

        for media_file in advertisement_images:
            models.AdvertisementImage.objects.create(advertisement=advertisement, image=media_file)

        return advertisement

    def update(self, instance, validated_data):
        advertisement_images = validated_data.pop('images', [])
        current_images_count = instance.advertisement_images.count()

        # Validate number of images
        package = instance.subscription.package if instance.subscription.package_category == 1 else instance.subscription.custom_package
        if len(advertisement_images) + current_images_count > package.number_of_image:
            raise serializers.ValidationError("Number of images exceeds package limit")

        # Update fields of the Advertisement instance
        instance.title = validated_data.get('title', instance.title)
        instance.link = validated_data.get('link', instance.link)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # create AdvertisementImage instances
        for media_file in advertisement_images:
            models.AdvertisementImage.objects.create(advertisement=instance, image=media_file)

        return instance

    def get_expiry_date(self, obj):
        user = self.context['request'].user
        if obj.subscription:
            if obj.subscription.package_category == 1:
                subscription = models.Subscription.objects.filter(user=user, package=obj.subscription.package).last()
            else:
                subscription = models.Subscription.objects.filter(user=user, custom_package=obj.subscription.custom_package).last()
            if subscription:
                return subscription.expiry_date
        return None

    def get_active_date(self, obj):
        user = self.context['request'].user
        if obj.subscription:
            if obj.subscription.package_category == 1:
                subscription = models.Subscription.objects.filter(user=user, package=obj.subscription.package).last()
            else:
                subscription = models.Subscription.objects.filter(user=user, custom_package=obj.subscription.custom_package).last()
            if subscription:
                return subscription.created.date()
        return None


class PublicAdvertisementSerializer(DynamicFieldsUUIDModelSerializer):
    advertisement_images = AdvertisementImageSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False), write_only=True
    )
    subscription_details = SubscriptionSerializer(source="subscription", read_only=True)
    active_date = serializers.SerializerMethodField(read_only=True)
    expiry_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Advertisement
        fields = [
            "uuid", "subscription", "subscription_details", "title", "link", "is_active", "images",
            "advertisement_images", "active_date", "expiry_date", "response_message", "status"
        ]
    def get_expiry_date(self, obj):

        return None

    def get_active_date(self, obj):

        return None
