from rest_framework.routers import DefaultRouter
from hms_app.views import NurseViewSet, AppointmentRescheduleViewSet

router = DefaultRouter()
router.register(r'', NurseViewSet, basename='nurses')
router.register(r'appointments/reschedule', AppointmentRescheduleViewSet, basename='appointment_reschedule')

urlpatterns = router.urls
