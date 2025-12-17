"""
URL configuration for HMS
"""
from django.contrib import admin
from django.urls import path, include
from hms_app.template_views import HomeView, DoctorDashboardView, PatientDashboardView, NurseDashboardView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('dashboard/patient/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('dashboard/nurse/', NurseDashboardView.as_view(), name='nurse_dashboard'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('hms_app.urls.auth')),
    path('api/doctors/', include('hms_app.urls.doctors')),
    path('api/users/', include('hms_app.urls.users')),
    path('api/appointments/', include('hms_app.urls.appointments')),
    path('api/medical_reports/', include('hms_app.urls.medical_reports')),
    path('api/nurses/', include('hms_app.urls.nurses')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
