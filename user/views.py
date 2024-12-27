from rest_framework import permissions, status, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Follower, Profile
from .serializers import ProfileSerializer, FollowerSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            profile, created = Profile.objects.get_or_create(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"])
    def is_following(self, request, pk=None):
        followed_user = User.objects.get(pk=pk)
        is_following = Follower.objects.filter(follower=request.user, followed=followed_user).exists()
        return Response({"is_following": is_following}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        followed_user = User.objects.get(pk=pk)
        if request.user == followed_user:
            raise serializers.ValidationError("You cannot follow yourself")

        follower, created = Follower.objects.get_or_create(follower=request.user, followed=followed_user)
        if not created:
            raise serializers.ValidationError("You are already following this user")

        serializer = FollowerSerializer(follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def unfollow(self, request, pk=None):
        followed_user = User.objects.get(pk=pk)
        try:
            follower = Follower.objects.get(follower=request.user, followed=followed_user)
            follower.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follower.DoesNotExist:
            raise serializers.ValidationError("You are not following this user")

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        user = User.objects.get(pk=pk)
        followers = Follower.objects.filter(followed=user)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        user = User.objects.get(pk=pk)
        following = Follower.objects.filter(follower=user)
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get", "post", "put", "patch"])
    def profile(self, request):
        try:
            if request.method == "POST":
                if hasattr(request.user, "profile"):
                    return Response({"detail": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = ProfileSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            profile = request.user.profile
            if request.method == "GET":
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method in ["PUT", "PATCH"]:
                serializer = ProfileSerializer(profile, data=request.data, partial=request.method == "PATCH")
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
