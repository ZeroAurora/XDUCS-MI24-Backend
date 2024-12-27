from rest_framework import serializers
from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ["id", "file", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]
