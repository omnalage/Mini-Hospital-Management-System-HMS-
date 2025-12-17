#!/usr/bin/env python
"""
Populate the database with sample data for testing
Run this after migrations with: python manage.py shell < populate_db.py
"""

from django.contrib.auth.models import User
from hms_app.models import UserProfile, Doctor, DoctorAvailability, Appointment
from datetime import datetime, time
import django

django.setup()

# Clear existing data
print("Clearing existing data...")
User.objects.all().delete()

# Create sample doctors
print("Creating sample doctors...")
doctors_data = [
    {
        'username': 'dr_smith',
        'email': 'dr.smith@hms.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'password': 'DoctorPass123',
        'specialization': 'Cardiology',
        'license': 'LIC001',
        'experience': 10
    },
    {
        'username': 'dr_johnson',
        'email': 'dr.johnson@hms.com',
        'first_name': 'Robert',
        'last_name': 'Johnson',
        'password': 'DoctorPass123',
        'specialization': 'Dermatology',
        'license': 'LIC002',
        'experience': 8
    },
    {
        'username': 'dr_brown',
        'email': 'dr.brown@hms.com',
        'first_name': 'Mary',
        'last_name': 'Brown',
        'password': 'DoctorPass123',
        'specialization': 'Neurology',
        'license': 'LIC003',
        'experience': 12
    },
]

doctors = []
for doc_data in doctors_data:
    user = User.objects.create_user(
        username=doc_data['username'],
        email=doc_data['email'],
        first_name=doc_data['first_name'],
        last_name=doc_data['last_name'],
        password=doc_data['password']
    )
    
    UserProfile.objects.create(
        user=user,
        role='doctor',
        phone_number='9876543210'
    )
    
    doctor = Doctor.objects.create(
        user=user,
        specialization=doc_data['specialization'],
        license_number=doc_data['license'],
        experience_years=doc_data['experience'],
        consultation_fee=500
    )
    
    doctors.append(doctor)
    print(f"✓ Created doctor: Dr. {doc_data['first_name']} {doc_data['last_name']}")

# Create availability slots for doctors
print("\nCreating availability slots...")
availability_data = [
    {'day': 'MON', 'start': '09:00', 'end': '12:00'},
    {'day': 'MON', 'start': '14:00', 'end': '17:00'},
    {'day': 'WED', 'start': '09:00', 'end': '12:00'},
    {'day': 'FRI', 'start': '10:00', 'end': '13:00'},
]

for doctor in doctors:
    for avail in availability_data:
        DoctorAvailability.objects.create(
            doctor=doctor,
            day_of_week=avail['day'],
            start_time=datetime.strptime(avail['start'], '%H:%M').time(),
            end_time=datetime.strptime(avail['end'], '%H:%M').time(),
            is_active=True
        )
    print(f"✓ Created availability slots for Dr. {doctor.user.first_name}")

# Create sample patients
print("\nCreating sample patients...")
patients_data = [
    {
        'username': 'john_doe',
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'PatientPass123'
    },
    {
        'username': 'jane_patient',
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Patient',
        'password': 'PatientPass123'
    },
]

for pat_data in patients_data:
    user = User.objects.create_user(
        username=pat_data['username'],
        email=pat_data['email'],
        first_name=pat_data['first_name'],
        last_name=pat_data['last_name'],
        password=pat_data['password']
    )
    
    UserProfile.objects.create(
        user=user,
        role='patient',
        phone_number='9123456789'
    )
    
    print(f"✓ Created patient: {pat_data['first_name']} {pat_data['last_name']}")

print("\n" + "="*50)
print("✓ Database populated successfully!")
print("="*50)
print("\nTest Login Credentials:")
print("\nDoctors:")
for doc in doctors_data:
    print(f"  Username: {doc['username']}, Password: {doc['password']}")
print("\nPatients:")
for pat in patients_data:
    print(f"  Username: {pat['username']}, Password: {pat['password']}")
print("\n" + "="*50)
