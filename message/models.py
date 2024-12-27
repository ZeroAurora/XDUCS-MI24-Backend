from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["sender", "recipient"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_delivered(self):
        self.is_delivered = True
        self.save()


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="status")
    is_online = models.BooleanField(default=False)
    is_typing = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Online" if self.is_online else "Offline"
        typing = " (typing)" if self.is_typing else ""
        return f"{self.user.username} - {status}{typing}"
