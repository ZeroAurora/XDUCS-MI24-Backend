from rest_framework import serializers
from .models import Post, Comment, Like
from user.serializers import DjangoUserSerializer
from file.serializers import MediaFileSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at", "updated_at"]


class LikeSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer(read_only=True)
    media_files = MediaFileSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "content", "created_at", "updated_at", "media_files", "comments", "likes"]
