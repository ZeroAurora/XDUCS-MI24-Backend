from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, FollowRelationship


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "bio",
            "profile_picture",
            "background_image",
            "date_of_birth",
            "location",
            "following_count",
            "follower_count",
        ]

    def get_following_count(self, obj):
        return obj.user.following.count()

    def get_follower_count(self, obj):
        return obj.user.followers.count()


class FollowingSerializer(serializers.ModelSerializer):
    followed = DjangoUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FollowRelationship
        fields = ["id", "followed", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    follower = DjangoUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FollowRelationship
        fields = ["id", "follower", "created_at"]


class FollowRelationshipSerializer(serializers.ModelSerializer):
    follower = DjangoUserSerializer(read_only=True)
    followed = DjangoUserSerializer(read_only=True)

    class Meta:
        model = FollowRelationship
        fields = ["id", "follower", "followed", "created_at"]
