from django.db import models
from django.contrib.auth.models import User
from file.models import MediaFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    background_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class FollowRelationship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
