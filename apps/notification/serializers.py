from rest_framework import serializers
from datetime import date

class PurchaseNotificationSerializer(serializers.Serializer):
    package_name = serializers.CharField(max_length=255)
    order_number = serializers.CharField(max_length=255)
    total_amount = serializers.IntegerField()
    date = serializers.DateField(default=date.today)
class SellpostApprovedNotificationSerializer(serializers.Serializer):
    post_id = serializers.UUIDField(required=True)

class PaymentSuccessfullNotificationSerializer(serializers.Serializer):
    package_id = serializers.UUIDField(required=True)

