from rest_framework import serializers
from .models import Notification
from post.serializers import ContentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    source_user = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            "id",
            "source_user",
            "content",
            "notification_type",
            "created_at",
            "is_read"
        ]
        read_only_fields = ["created_at", "is_read"]

    def get_source_user(self, obj):
        return obj.content.user.id