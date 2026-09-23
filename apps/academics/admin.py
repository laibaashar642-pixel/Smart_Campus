from django.contrib import admin


from .models import Course, Department, Enrollment, Section

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Enrollment)