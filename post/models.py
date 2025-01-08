from django.db import models
from django.contrib.auth.models import User

from file.models import MediaFile


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    media_files = models.ManyToManyField(MediaFile, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.is_post:
            return f"Post by {self.user.username} at {self.created_at}"
        return f"Comment by {self.user.username} on {self.parent}"

    @property
    def is_post(self):
        return self.parent is None

    @property
    def is_comment(self):
        return self.parent is not None and self.parent.is_post

    @property
    def is_reply(self):
        return self.parent is not None and self.parent.is_comment


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content")

    def __str__(self):
        return f"Like by {self.user.username} on {self.content}"
