from django.urls import path
from rest_framework.routers import DefaultRouter
from hms_app.views import SignUpView

router = DefaultRouter()
router.register(r'', SignUpView, basename='auth')

urlpatterns = router.urls
