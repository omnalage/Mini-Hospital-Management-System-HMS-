from django.urls import path
from rest_framework.routers import DefaultRouter
from hms_app.views import AppointmentViewSet

router = DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointments')

urlpatterns = router.urls
