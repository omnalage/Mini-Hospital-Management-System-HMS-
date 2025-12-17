from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    """Extended user profile for role-based access"""
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"
    
    class Meta:
        ordering = ['-created_at']


class Doctor(models.Model):
    """Doctor profile with specialization and qualifications"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, default='General Practitioner')
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(validators=[MinValueValidator(0)])
    bio = models.TextField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class DoctorAvailability(models.Model):
    """Time slots available for doctor consultations"""
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.doctor} - {self.day_of_week} {self.start_time} to {self.end_time}"
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week', 'start_time', 'end_time']


class Appointment(models.Model):
    """Patient appointments with doctors"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        patient_name = self.patient.get_full_name() or self.patient.username
        return f"{patient_name} - {self.doctor} on {self.appointment_date}"
    
    class Meta:
        ordering = ['-appointment_date', '-start_time']
        unique_together = ['doctor', 'appointment_date', 'start_time']
