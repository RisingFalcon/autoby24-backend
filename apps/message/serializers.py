# serializers.py
from rest_framework import serializers
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'email', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['uuid', 'sender', 'receiver', 'content', 'created_at', 'is_read', 'is_archived', 'is_resolved']
        read_only_fields = ['uuid', 'created_at', 'is_read', 'is_archived', 'is_resolved']

class CreateMessageSerializer(serializers.ModelSerializer):
    receiver_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['receiver_id', 'content']

    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        sender = self.context['request'].user
        try:
            receiver = User.objects.get(uuid=receiver_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found")
        
        return Message.objects.create(sender=sender, receiver=receiver, **validated_data)