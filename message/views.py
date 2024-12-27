from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from message.models import Message, UserStatus
from message.serializers import MessageSerializer, UserStatusSerializer
from django.utils import timezone


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by("-timestamp")

    def perform_create(self, serializer):
        recipient = get_object_or_404(User, username=self.request.data.get("recipient"))
        serializer.save(sender=self.request.user, recipient=recipient)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        if message.recipient == request.user:
            message.mark_as_read()
            return Response({"status": "message marked as read"})
        return Response(
            {"error": "You can only mark your received messages as read"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=False, methods=["get"])
    def conversation(self, request):
        other_user = get_object_or_404(User, username=request.query_params.get("with"))
        messages = Message.objects.filter(
            Q(sender=request.user, recipient=other_user) | Q(sender=other_user, recipient=request.user)
        ).order_by("timestamp")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


class UserStatusViewSet(viewsets.ModelViewSet):
    serializer_class = UserStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserStatus.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def set_online(self, request):
        status_obj, _ = UserStatus.objects.get_or_create(user=request.user)
        status_obj.is_online = True
        status_obj.last_seen = timezone.now()
        status_obj.save()
        return Response({"status": "online"})

    @action(detail=False, methods=["post"])
    def set_offline(self, request):
        status_obj, _ = UserStatus.objects.get_or_create(user=request.user)
        status_obj.is_online = False
        status_obj.last_seen = timezone.now()
        status_obj.save()
        return Response({"status": "offline"})

    @action(detail=False, methods=["post"])
    def set_typing(self, request):
        status_obj, _ = UserStatus.objects.get_or_create(user=request.user)
        status_obj.is_typing = True
        status_obj.save()
        return Response({"status": "typing"})

    @action(detail=False, methods=["post"])
    def stop_typing(self, request):
        status_obj, _ = UserStatus.objects.get_or_create(user=request.user)
        status_obj.is_typing = False
        status_obj.save()
        return Response({"status": "stopped typing"})
