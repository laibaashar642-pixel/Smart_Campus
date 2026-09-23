"""Face enrollment API views."""
from rest_framework import permissions, viewsets

from .cv.embedder import get_face_encoding
from .models import FaceProfile
from .serializers import FaceProfileSerializer


class FaceProfileViewSet(viewsets.ModelViewSet):
    serializer_class = FaceProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return FaceProfile.objects.filter(student=user)
        return FaceProfile.objects.all()  # admin/teacher can view all

    def perform_create(self, serializer):
        # Students enroll their own face; admin could do it for them too
        instance = serializer.save(student=self.request.user)
        encoding = get_face_encoding(instance.enrollment_photo.path)
        if encoding is not None:
            instance.embedding = encoding
            instance.is_processed = True
            instance.save()