from rest_framework import serializers
from .models import Notification
from user.serializers import ProfileSerializer
from post.serializers import ContentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    content = ContentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "profile",
            "content",
            "notification_type",
            "created_at",
            "is_read"
        ]
        read_only_fields = ["created_at", "is_read"]

    def get_profile(self, obj):
        return ProfileSerializer(obj.user.profile).data
