from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate, login, logout
import logging
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import UserProfile, Doctor, DoctorAvailability, Appointment
from .models import MedicalReport
from .serializers import (
    UserSerializer, UserProfileSerializer, DoctorSerializer, 
    DoctorAvailabilitySerializer, AppointmentSerializer,
    SignUpSerializer, DoctorSignUpSerializer
    , MedicalReportSerializer
)
from .permissions import IsDoctorOrReadOnly, IsPatientOrReadOnly, IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


# Authentication Views
class SignUpView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def patient_signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Patient registered successfully',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def doctor_signup(self, request):
        serializer = DoctorSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Doctor registered successfully',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.info('Login attempt for username=%s', username)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('Authentication successful for username=%s id=%s', username, user.id)
            # Ensure a UserProfile exists for this user; create a default patient profile if absent
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'patient',
                    'phone_number': ''
                }
            )
            if created:
                logger.info('UserProfile auto-created for username=%s', username)

            # Log session info when available
            try:
                session_key = request.session.session_key
                logger.info('Session key after login for username=%s: %s', username, session_key)
            except Exception:
                logger.debug('No session key available after login for username=%s', username)

            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': profile.role
            })
        return Response({
            'error': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        # Return JSON-friendly error codes instead of allowing the permission system
        if not request.user or not request.user.is_authenticated:
            logger.info('current_user request unauthenticated')
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            logger.warning('current_user: profile not found for user id=%s', request.user.id)
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile)
        return Response({'user': serializer.data})


# Doctor Views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Doctors see only their own profile, patients see all available doctors
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'doctor':
                return Doctor.objects.filter(user=user)
            else:
                return Doctor.objects.filter(is_available=True)
        except UserProfile.DoesNotExist:
            return Doctor.objects.none()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = self.get_serializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        doctor = self.get_object()
        slots = DoctorAvailability.objects.filter(doctor=doctor, is_active=True)
        serializer = DoctorAvailabilitySerializer(slots, many=True)
        return Response(serializer.data)


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        try:
            doctor = Doctor.objects.get(user=user)
            return DoctorAvailability.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return DoctorAvailability.objects.none()
    
    def perform_create(self, serializer):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            serializer.save(doctor=doctor)
        except Doctor.DoesNotExist:
            raise NotFound('Doctor profile not found')
    
    def perform_update(self, serializer):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
            serializer.save(doctor=doctor)
        except Doctor.DoesNotExist:
            raise NotFound('Doctor profile not found')


# Appointment Views
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'doctor':
                doctor = Doctor.objects.get(user=user)
                return Appointment.objects.filter(doctor=doctor)
            else:
                return Appointment.objects.filter(patient=user)
        except (UserProfile.DoesNotExist, Doctor.DoesNotExist):
            return Appointment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
    
    @action(detail=False, methods=['post'])
    def book_appointment(self, request):
        doctor_id = request.data.get('doctor_id')
        appointment_date = request.data.get('appointment_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        reason = request.data.get('reason', '')
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if appointment already exists
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            start_time=start_time,
            status='scheduled'
        ).exists():
            return Response({'error': 'Time slot already booked'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            reason=reason,
            status='scheduled'
        )
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel_appointment(self, request, pk=None):
        appointment = self.get_object()
        if appointment.patient != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        appointment.status = 'cancelled'
        appointment.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class MedicalReportViewSet(viewsets.ModelViewSet):
    """ViewSet for creating and viewing medical reports. Doctors can create and view reports for patients they have appointments with; doctors can view history."""
    serializer_class = MedicalReportSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        # If doctor, return reports for patients the doctor has seen; otherwise patients can see their own reports
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return MedicalReport.objects.none()

        if profile.role == 'doctor':
            try:
                doctor = Doctor.objects.get(user=user)
                # Reports written by this doctor or for patients this doctor has appointments with
                patient_ids = Appointment.objects.filter(doctor=doctor).values_list('patient', flat=True).distinct()
                return MedicalReport.objects.filter(patient__in=patient_ids)
            except Doctor.DoesNotExist:
                return MedicalReport.objects.none()
        else:
            # patient: only their own reports
            return MedicalReport.objects.filter(patient=user)

    def perform_create(self, serializer):
        # Allow doctor's user to attach their Doctor record when creating
        user = self.request.user
        try:
            doctor = Doctor.objects.get(user=user)
            serializer.save(doctor=doctor)
        except Doctor.DoesNotExist:
            # allow admin/staff to create without doctor
            serializer.save()

    def list(self, request, *args, **kwargs):
        # Support filtering by patient_id via query param
        qs = self.get_queryset()
        patient_id = request.query_params.get('patient_id')
        if patient_id:
            try:
                patient = User.objects.get(id=patient_id)
            except User.DoesNotExist:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

            # If requester is doctor, verify they have appointments with this patient
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

            if profile.role == 'doctor':
                try:
                    doctor = Doctor.objects.get(user=request.user)
                    if not Appointment.objects.filter(doctor=doctor, patient=patient).exists():
                        return Response({'error': 'No access to this patient'}, status=status.HTTP_403_FORBIDDEN)
                except Doctor.DoesNotExist:
                    return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # patients can only request their own id
                if request.user.id != int(patient_id):
                    return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

            qs = qs.filter(patient=patient)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
