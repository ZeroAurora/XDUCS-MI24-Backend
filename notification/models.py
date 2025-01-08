from django.db import models
from django.conf import settings
from post.models import Post, Comment


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("reply", "Reply"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="+")
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.post:
            return f"{self.get_notification_type_display()} on post {self.post.id} by {self.user.username}"
        elif self.comment:
            return f"{self.get_notification_type_display()} on comment {self.comment.id} by {self.user.username}"
