
from django.contrib import admin

from .models import FaceProfile


@admin.register(FaceProfile)
class FaceProfileAdmin(admin.ModelAdmin):
    list_display = ("student", "is_processed", "created_at")
    readonly_fields = ("embedding", "is_processed")