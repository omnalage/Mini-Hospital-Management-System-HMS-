from django.urls import path
from rest_framework.routers import DefaultRouter
from hms_app.views import DoctorViewSet, DoctorAvailabilityViewSet

router = DefaultRouter()
router.register(r'', DoctorViewSet, basename='doctors')
router.register(r'availability', DoctorAvailabilityViewSet, basename='availability')

urlpatterns = router.urls
