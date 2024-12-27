from rest_framework import serializers
from message.models import Message, UserStatus
from user.serializers import UserSerializer


class UserStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserStatus
        fields = ["user", "is_online", "is_typing", "last_seen"]
        read_only_fields = ["last_seen"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "recipient",
            "content",
            "timestamp",
            "is_read",
            "is_delivered",
        ]
        read_only_fields = ["id", "timestamp", "is_read", "is_delivered"]
