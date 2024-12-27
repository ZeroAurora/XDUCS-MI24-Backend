from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "profile_picture", "date_of_birth", "location"]


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "follower", "followed", "created_at"]
