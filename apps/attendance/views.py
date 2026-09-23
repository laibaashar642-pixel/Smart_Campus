"""Attendance API views."""
from rest_framework import permissions, viewsets

from apps.accounts.permissions import IsTeacher

from .models import AttendanceRecord, ClassSession
from .serializers import AttendanceRecordSerializer, ClassSessionSerializer


class ClassSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSessionSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = ClassSession.objects.select_related("section").prefetch_related("records")
        if user.role == "teacher":
            return qs.filter(section__teacher=user)
        if user.role == "student":
            return qs.filter(section__enrollments__student=user).distinct()
        return qs  # admin sees all

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = AttendanceRecord.objects.select_related("session", "student")
        if user.role == "teacher":
            return qs.filter(session__section__teacher=user)
        if user.role == "student":
            return qs.filter(student=user)
        return qs