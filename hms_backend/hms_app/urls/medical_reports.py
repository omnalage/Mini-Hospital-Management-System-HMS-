from rest_framework.routers import DefaultRouter
from hms_app.views import MedicalReportViewSet

router = DefaultRouter()
router.register(r'', MedicalReportViewSet, basename='medical_reports')

urlpatterns = router.urls
