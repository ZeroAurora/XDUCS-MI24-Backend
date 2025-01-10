from rest_framework import serializers
from .models import Content, Like
from user.serializers import ProfileSerializer
from file.serializers import MediaFileSerializer


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class ContentSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    media_files = MediaFileSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "profile",
            "content",
            "created_at",
            "updated_at",
            "media_files",
            "likes",
        ]

    def get_profile(self, obj):
        return ProfileSerializer(obj.user.profile).data
