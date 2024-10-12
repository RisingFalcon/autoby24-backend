from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from rest_framework import serializers
from apps.core.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer
)
from apps.users import models
from base.validators import validate_international_phone_number
from base.globals import UserConstants

class UserRegistrationSerializer(DynamicFieldsUUIDModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model = models.User
        fields = [
            "uuid", "user_type", "email", "is_email_verify", "first_name", "last_name", "mobile_number", "password",
            "is_profile_update", "country"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        custom_user = super().create(validated_data)
        if password is not None:
            custom_user.set_password(password)
        custom_user.save()
        return custom_user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class DealerAvailabilitySerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = models.DealerAvailability
        fields = ['day_of_week', 'from_time', 'to_time', 'is_off_day']


class UserProfileSerializer(DynamicFieldsUUIDModelSerializer):
    availability = DealerAvailabilitySerializer(many=True)
    country = CountrySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = models.User
        fields = [
            'id', 'first_name', 'last_name', 'mobile_number', 'whatsapp_number', 
            'email', 'user_type', 'country', 'state', 'city', 'postal_code', 
            'street_number', 'street_name', 'date_of_birth', 'road_number', 
            'house_number', 'biography', 'profile_picture', 'dealership_name', 
            'address', 'company_registration_number', 'company_website', 
            'is_email_verify', 'is_google_verify', 'is_facebook_verify', 
            'facebook_id', 'is_active', 'is_staff', 'is_superuser', 'date_joined',
            'cover_image', 'availability',
        ]
    def create(self, validated_data):
        availability_data = validated_data.pop('availability', [])
        user = models.User.objects.create(**validated_data)
        
        # Create or update availability records
        for availability in availability_data:
            models.DealerAvailability.objects.create(dealer=user, **availability)
        
        return user

    def update(self, instance, validated_data):
        availability_data = validated_data.pop('availability', [])
        instance = super().update(instance, validated_data)

        # Update or create availability records
        for availability in availability_data:
            day_of_week = availability.get('day_of_week')
            avail_instance = models.DealerAvailability.objects.filter(dealer=instance, day_of_week=day_of_week).first()

            if avail_instance:
                # If it exists, update the existing record
                avail_instance.from_time = availability.get('from_time', avail_instance.from_time)
                avail_instance.to_time = availability.get('to_time', avail_instance.to_time)
                avail_instance.is_off_day = availability.get('is_off_day', avail_instance.is_off_day)
                avail_instance.save()
            else:
                models.DealerAvailability.objects.create(dealer=instance, **availability)

        return instance

    def get_availability(self, obj):
        if obj.user_type == 3:
            availability = obj.availability.all()
            return DealerAvailabilitySerializer(availability, many=True).data
        return None

# class UserProfileSerializer(DynamicFieldsUUIDModelSerializer):
#     country_name = serializers.CharField(source="country__name", read_only=True)
#     state_name = serializers.CharField(source="state__name", read_only=True)

#     class Meta:
#         model = models.User
#         fields = [
#             "uuid", "user_type", "email", "first_name", "last_name", "profile_picture", "mobile_number", "country",
#             "date_of_birth", "road_number", "house_number", "biography", "whatsapp_number", "state", "country_name",
#             "state_name", "dealership_name", "address", "company_registration_number", "company_website",
#             "is_email_verify", "is_google_verify", "is_facebook_verify", "is_active", "date_joined", "modified",
#             "created", "response_message"
#         ]

#     # def update(self, instance, validated_data):
#     #     instance = super().update(instance, validated_data)
#     #     if "mobile_number" in validated_data:
#     #         validate_international_phone_number(validated_data['mobile_number'],
#     #                                             "mobile_number")
#     #     return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=4)
    uid = serializers.CharField()
    token = serializers.CharField()

class DealerPublicProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    dealership_name = serializers.CharField()
    city = serializers.CharField(allow_null=True)
    postal_code = serializers.CharField(allow_null=True)
    country = serializers.CharField(allow_null=True)
    biography = serializers.CharField(allow_null=True)
    rating = serializers.FloatField(allow_null=True)
    total_review = serializers.IntegerField()
    email = serializers.EmailField()
    whatsapp_number = serializers.CharField(allow_null=True)
    profile_picture = serializers.URLField(allow_null=True)
    cover_image = serializers.URLField(allow_null=True)
    distance = serializers.FloatField(allow_null=True)

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserReview
        fields = ['uuid', 'dealer_id', 'client_id', 'product_type', 'product_id','rating', 'review_text', 'timestamp']
        read_only_fields = ['uuid', 'dealer_id', 'client_id', 'timestamp']