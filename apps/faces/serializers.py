"""Face API serializers."""
from rest_framework import serializers

from .models import FaceProfile


class FaceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceProfile
        fields = ["id", "student", "enrollment_photo", "is_processed", "created_at"]
        read_only_fields = ["is_processed"]