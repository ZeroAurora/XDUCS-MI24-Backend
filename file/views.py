from rest_framework import permissions, viewsets, parsers
from .models import MediaFile
from .serializers import MediaFileSerializer


class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    parser_classes = [parsers.FileUploadParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
