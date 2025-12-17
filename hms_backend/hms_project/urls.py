"""
URL configuration for HMS
"""
from django.contrib import admin
from django.urls import path, include
from hms_app.template_views import HomeView, DoctorDashboardView, PatientDashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('dashboard/patient/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('hms_app.urls.auth')),
    path('api/doctors/', include('hms_app.urls.doctors')),
    path('api/appointments/', include('hms_app.urls.appointments')),
]
