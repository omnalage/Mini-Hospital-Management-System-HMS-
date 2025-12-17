from django.contrib import admin
from .models import UserProfile, Doctor, DoctorAvailability, Appointment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'specialization', 'license_number', 'is_available']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = "Doctor Name"


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'start_time', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__username', 'doctor__user__first_name', 'doctor__user__last_name']
