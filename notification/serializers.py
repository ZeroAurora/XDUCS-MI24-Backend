from rest_framework import serializers
from .models import Notification
from user.serializers import DjangoUserSerializer
from post.serializers import PostSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "post", "comment", "notification_type", "created_at", "is_read"]
        read_only_fields = ["created_at", "is_read"]
