from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Content, Like
from .serializers import ContentSerializer, LikeSerializer
from file.models import MediaFile


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.filter(parent__isnull=True)  # Only top-level posts
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        content = serializer.save(user=self.request.user)
        media_file_ids = self.request.data.get("media_files", [])
        media_files = MediaFile.objects.filter(id__in=media_file_ids, owner=self.request.user)
        content.media_files.set(media_files)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        content = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, content=content)
        if not created:
            return Response({"detail": "You already liked this content"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        content = self.get_object()
        try:
            like = Like.objects.get(user=request.user, content=content)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this content"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=["get"])
    def likes(self, request, pk=None):
        content = self.get_object()
        likes = Like.objects.filter(content=content)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def comments(self, request, pk=None):
        content = self.get_object()
        if request.method == "POST":
            serializer = ContentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, parent=content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        comments = Content.objects.filter(parent=content)
        serializer = ContentSerializer(comments, many=True)
        return Response(serializer.data)
