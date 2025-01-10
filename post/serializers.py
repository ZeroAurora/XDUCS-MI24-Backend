from rest_framework import serializers
from .models import Content, Like
from user.serializers import ProfileSerializer
from file.serializers import MediaFileSerializer


class LikeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "profile", "created_at"]
    
    def get_profile(self, obj):
        return ProfileSerializer(obj.user.profile).data


class ContentSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    media_files = MediaFileSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "profile",
            "content",
            "created_at",
            "updated_at",
            "media_files",
            "like_count",
        ]

    def get_profile(self, obj):
        return ProfileSerializer(obj.user.profile).data
    
    def get_like_count(self, obj):
        return obj.likes.count()
