from rest_framework.routers import DefaultRouter

from .views import FaceProfileViewSet

router = DefaultRouter()
router.register("profiles", FaceProfileViewSet, basename="face-profile")

urlpatterns = router.urls