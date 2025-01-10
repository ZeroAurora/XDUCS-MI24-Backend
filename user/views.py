from rest_framework import permissions, status, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Profile, FollowRelationship
from .serializers import ProfileSerializer, FollowerSerializer, FollowingSerializer, FollowRelationshipSerializer


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # Profile actions
    @action(detail=False, methods=["get", "put"])
    def me(self, request):
        """Get or update current user's profile"""
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        if request.method == "GET":
            serializer = ProfileSerializer(profile, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def profile(self, request, pk=None):
        """Get another user's profile"""
        try:
            user = User.objects.get(pk=pk)
            profile, created = Profile.objects.get_or_create(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found."})

    # Follow actions
    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        """Follow another user"""
        followed_user = User.objects.get(pk=pk)
        if request.user == followed_user:
            raise serializers.ValidationError({"detail": "You cannot follow yourself"})

        follower, created = FollowRelationship.objects.get_or_create(follower=request.user, followed=followed_user)
        if not created:
            raise serializers.ValidationError({"detail": "You are already following this user"})

        serializer = FollowRelationshipSerializer(follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        """Unfollow another user"""
        followed_user = User.objects.get(pk=pk)
        try:
            relationship = FollowRelationship.objects.get(follower=request.user, followed=followed_user)
            relationship.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FollowRelationship.DoesNotExist:
            raise serializers.ValidationError({"detail": "You are not following this user"})

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        """Get a user's followers"""
        user = User.objects.get(pk=pk)
        followers = FollowRelationship.objects.filter(followed=user)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        """Get users a user is following"""
        user = User.objects.get(pk=pk)
        following = FollowRelationship.objects.filter(follower=user)
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def is_following(self, request, pk=None):
        """Check if a user is following another user"""
        followed_user = User.objects.get(pk=pk)
        following = FollowRelationship.objects.filter(follower=request.user, followed=followed_user)
        if following.exists():
            return Response({"is_following": True}, status=status.HTTP_200_OK)
        return Response({"is_following": False}, status=status.HTTP_200_OK)
