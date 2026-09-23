"""Attendance API serializers."""
from rest_framework import serializers

from .models import AttendanceRecord, ClassSession


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            "id", "session", "student", "student_name",
            "status", "marked_by", "confidence", "reviewed",
        ]
        read_only_fields = ["marked_by", "confidence"]


class ClassSessionSerializer(serializers.ModelSerializer):
    records = AttendanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = ClassSession
        fields = [
            "id", "section", "date", "topic", "class_photo",
            "status", "created_by", "created_at", "records",
        ]
        read_only_fields = ["status", "created_by", "created_at"]