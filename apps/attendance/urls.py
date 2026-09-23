from rest_framework.routers import DefaultRouter

from .views import AttendanceRecordViewSet, ClassSessionViewSet

router = DefaultRouter()
router.register("sessions", ClassSessionViewSet, basename="session")
router.register("records", AttendanceRecordViewSet, basename="record")

urlpatterns = router.urls