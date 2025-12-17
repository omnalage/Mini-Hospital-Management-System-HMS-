from django.urls import path
from rest_framework.routers import DefaultRouter
from hms_app.views import DoctorViewSet, DoctorAvailabilityViewSet

router = DefaultRouter()
# Register availability first so the empty-prefix DoctorViewSet detail route
# doesn't accidentally capture the 'availability' path as a lookup value.
router.register(r'availability', DoctorAvailabilityViewSet, basename='availability')
router.register(r'', DoctorViewSet, basename='doctors')

urlpatterns = router.urls
