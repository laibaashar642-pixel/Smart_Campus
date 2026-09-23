"""Academic domain models."""
from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code


class Course(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="courses"
    )
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150)
    credit_hours = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Section(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="teaching_sections",
        limit_choices_to={"role": "teacher"},
    )
    name = models.CharField(max_length=20)   # e.g. "A"
    term = models.CharField(max_length=20)   # e.g. "Fall 2026"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "name", "term"], name="unique_section"
            )
        ]

    def __str__(self):
        return f"{self.course.code}-{self.name} ({self.term})"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "student"},
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "section"], name="unique_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.student} -> {self.section}"