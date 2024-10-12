from dj_rest_kit.serializers import DynamicFieldsUUIDModelSerializer
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from apps.package.serializers import SubscriptionSerializer
from apps.users.serializers import UserProfileSerializer
from .models import (
    Transactions,
    Payment,
    Donation
)


class PaymentSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class TransactionSerializer(DynamicFieldsUUIDModelSerializer):
    subscription_detail = SubscriptionSerializer(source="subscription", read_only=True)
    user_detail = UserProfileSerializer(source="user", read_only=True)
    
    class Meta:
        model = Transactions
        fields = ["id", "uuid", "transaction_id", "status", "subscription", "user", "creation_date", "updated_on", "created", "modified",
                    "subscription_detail", "user_detail"  
                ]


class DonationSerializer(DynamicFieldsUUIDModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"

class TransactionListSerializer(DynamicFieldsUUIDModelSerializer):
    user_details = serializers.SerializerMethodField()
    report = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()

    class Meta:
        model = Transactions
        fields = ["id", "user_details", "report", "type", "action"]

    def get_user_details(self, obj):
        user = obj.user
        return {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "is_new": user.date_joined > (timezone.now() - timedelta(days=30))
        }

    def get_report(self, obj):
        # implement actual report logic here, we need to create a new view for this or it should be removed from design
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla..."

    def get_type(self, obj):
        package_category = obj.subscription.package_category
        package_types = {
            1: "Car Sell Package Purchase",
            2: "Bike Sell Package Purchase",
            3: "Local Sell Package Purchase",
            4: "VIP Package Purchase",
            5: "Rent a Car Package Purchase",
            6: "Rent a Bike Package Purchase",
            7: "Rent a Garage Package Purchase",
            8: "Component Package Purchase",
            9: "Promotional Rent a Car Package Purchase",
            10: "Promotional Rent a Bike Package Purchase",
            11: "Promotional Rent a Garage Package Purchase"
        }
        
        return package_types.get(package_category, "Support & Inquiry")

    def get_action(self, obj):
        # This could be a link or an action identifier
        return "View More"