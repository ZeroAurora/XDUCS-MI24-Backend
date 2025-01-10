import uuid
import os
from django.db import models
from django.contrib.auth import get_user_model


def generate_random_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"media_files/{instance.id}{ext}"


User = get_user_model()


class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=generate_random_filename)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="media_files")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Media file by {self.owner.username}"

    def get_absolute_url(self):
        return self.file.url
