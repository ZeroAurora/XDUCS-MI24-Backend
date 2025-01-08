from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile, Follower
from .serializers import ProfileSerializer, FollowerSerializer, FollowingSerializer, FollowRelationshipSerializer


class UserProfileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            user = User.objects.get(pk=self.kwargs["pk"])
            profile, created = Profile.objects.get_or_create(user=user)
            return profile
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found."})


class UserFollowView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowRelationshipSerializer

    def create(self, request, *args, **kwargs):
        followed_user = User.objects.get(pk=self.kwargs["pk"])
        if request.user == followed_user:
            raise serializers.ValidationError({"detail": "You cannot follow yourself"})

        follower, created = Follower.objects.get_or_create(follower=request.user, followed=followed_user)
        if not created:
            raise serializers.ValidationError({"detail": "You are already following this user"})

        serializer = self.get_serializer(follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserUnfollowView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowRelationshipSerializer

    def get_object(self):
        followed_user = User.objects.get(pk=self.kwargs["pk"])
        try:
            return Follower.objects.get(follower=self.request.user, followed=followed_user)
        except Follower.DoesNotExist:
            raise serializers.ValidationError({"detail": "You are not following this user"})


class UserFollowersListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return Follower.objects.filter(followed=user)


class UserFollowingListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return Follower.objects.filter(follower=user)


class CurrentUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
