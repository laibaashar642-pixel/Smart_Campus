from django.contrib import admin


from .models import AttendanceRecord, ClassSession


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("section", "date", "status", "created_by")
    list_filter = ("status", "section")
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("session", "student", "status", "marked_by", "reviewed")
    list_filter = ("status", "marked_by", "reviewed")