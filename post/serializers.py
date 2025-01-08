from rest_framework import serializers
from .models import Content, Like
from user.serializers import DjangoUserSerializer
from file.serializers import MediaFileSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class ContentSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)
    media_files = MediaFileSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "user",
            "content",
            "created_at",
            "updated_at",
            "media_files",
            "likes",
        ]
