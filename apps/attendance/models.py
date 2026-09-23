"""Attendance domain models."""
from django.conf import settings
from django.db import models

from apps.academics.models import Section


class ClassSession(models.Model):
    """One lecture/class meeting for a section, on a given date."""

    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="sessions"
    )
    date = models.DateField()
    topic = models.CharField(max_length=200, blank=True)
    class_photo = models.ImageField(upload_to="class_photos/", null=True, blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),       # created, no photo processed yet
        ("processing", "Processing"), # Celery job running
        ("review", "Needs Review"),   # AI done, waiting for teacher confirm
        ("confirmed", "Confirmed"),   # teacher approved
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_sessions",
        limit_choices_to={"role": "teacher"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "date"], name="unique_session_per_day"
            )
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.section} - {self.date}"


class AttendanceRecord(models.Model):
    """One student's attendance for one class session."""

    session = models.ForeignKey(
        ClassSession, on_delete=models.CASCADE, related_name="records"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        limit_choices_to={"role": "student"},
    )

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="absent")

    SOURCE_CHOICES = [
        ("ai", "AI Detected"),
        ("manual", "Manual"),
    ]
    marked_by = models.CharField(max_length=8, choices=SOURCE_CHOICES, default="manual")
    confidence = models.FloatField(null=True, blank=True)  # AI match confidence, 0-1

    reviewed = models.BooleanField(default=False)  # teacher confirmed this row
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"], name="unique_attendance_per_session"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"