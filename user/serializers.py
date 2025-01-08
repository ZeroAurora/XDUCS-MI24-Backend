from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follower


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "bio",
            "profile_picture",
            "date_of_birth",
            "location",
            "following_count",
            "follower_count",
            "is_following",
        ]

    def get_following_count(self, obj) -> int:
        return obj.following.count()

    def get_follower_count(self, obj) -> int:
        return obj.followers.count()

    def get_is_following(self, obj) -> bool:
        return obj.followers.filter(follower=self.context["request"].user).exists()


class FollowingSerializer(serializers.ModelSerializer):
    followed = DjangoUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "followed", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    follower = DjangoUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "follower", "created_at"]


class FollowRelationshipSerializer(serializers.ModelSerializer):
    follower = DjangoUserSerializer(read_only=True)
    followed = DjangoUserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "follower", "followed", "created_at"]
