"""Face enrollment and embedding models."""
from django.conf import settings
from django.db import models


class FaceProfile(models.Model):
    """Stores a student's face embedding for matching."""

    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="face_profile",
        limit_choices_to={"role": "student"},
    )
    enrollment_photo = models.ImageField(upload_to="face_enrollment/")
    # 128-d face encoding from face_recognition, stored as JSON list
    embedding = models.JSONField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FaceProfile({self.student})"