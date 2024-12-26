from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "profile_picture", "date_of_birth", "location", "is_following"]

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Follower.objects.filter(follower=request.user, followed=obj.user).exists()
        return False


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "follower", "followed", "created_at"]
