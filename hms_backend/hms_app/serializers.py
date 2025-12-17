from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Doctor, DoctorAvailability, Appointment
from .models import MedicalReport, Nurse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'phone_number', 'created_at']


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    # doctor will be set server-side in the view's perform_create/perform_update
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'day_of_week', 'start_time', 'end_time', 'is_active']


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    availability_slots = DoctorAvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'license_number', 'experience_years', 
                  'bio', 'consultation_fee', 'is_available', 'availability_slots']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_name', 'patient', 'patient_name', 
                  'appointment_date', 'start_time', 'end_time', 'reason', 'status', 'notes']


class MedicalReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.SerializerMethodField(read_only=True)
    doctor_user = serializers.IntegerField(source='doctor.user.id', read_only=True, allow_null=True)
    nurse_user = serializers.IntegerField(source='nurse.user.id', read_only=True, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = MedicalReport
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_user', 'doctor_name', 'nurse_user', 'report_date', 'summary', 'details', 'file_url', 'file', 'created_at']

    def get_doctor_name(self, obj):
        """Return doctor full name or 'Staff' if no doctor is set."""
        if obj.doctor and obj.doctor.user:
            return obj.doctor.user.get_full_name() or obj.doctor.user.username
        return 'Staff'


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(choices=['doctor', 'patient', 'nurse'])
    phone_number = serializers.CharField(max_length=20, required=False)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        
        UserProfile.objects.create(
            user=user,
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number', ''),
        )
        
        return user


class DoctorSignUpSerializer(SignUpSerializer):
    specialization = serializers.CharField(max_length=100)
    license_number = serializers.CharField(max_length=50)
    experience_years = serializers.IntegerField(min_value=0)
    
    def create(self, validated_data):
        user = super().create(validated_data)
        
        Doctor.objects.create(
            user=user,
            specialization=validated_data['specialization'],
            license_number=validated_data['license_number'],
            experience_years=validated_data['experience_years'],
        )
        
        return user


class NurseSignUpSerializer(SignUpSerializer):
    employee_id = serializers.CharField(max_length=50)
    department = serializers.CharField(max_length=100, required=False)
    
    def create(self, validated_data):
        # Update role to nurse before parent create
        validated_data['role'] = 'nurse'
        user = super().create(validated_data)
        
        Nurse.objects.create(
            user=user,
            employee_id=validated_data['employee_id'],
            department=validated_data.get('department', ''),
        )
        
        return user


class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Nurse
        fields = ['id', 'user', 'employee_id', 'department', 'is_active']
