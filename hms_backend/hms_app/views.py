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
from .models import MedicalReport, Nurse
from .serializers import (
    UserSerializer, UserProfileSerializer, DoctorSerializer, 
    DoctorAvailabilitySerializer, AppointmentSerializer,
    SignUpSerializer, DoctorSignUpSerializer, NurseSignUpSerializer, NurseSerializer
    , MedicalReportSerializer
)
from .permissions import IsDoctorOrReadOnly, IsPatientOrReadOnly, IsOwnerOrReadOnly, IsReportAuthorOrNurseOrReadOnly

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
    def nurse_signup(self, request):
        serializer = NurseSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Nurse registered successfully',
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
            elif profile.role == 'nurse':
                # Nurses can see all appointments
                return Appointment.objects.all()
            else:
                return Appointment.objects.filter(patient=user)
        except (UserProfile.DoesNotExist, Doctor.DoesNotExist):
            return Appointment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
    
    @action(detail=False, methods=['post'])
    def book_appointment(self, request):
        from django.db import IntegrityError

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

        try:
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
        except IntegrityError as e:
            logger.error('IntegrityError booking appointment: %s', str(e))
            return Response({'error': 'This time slot is already booked. Please select a different time.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reschedule(self, request):
        """Reschedule an appointment (nurse or doctor) with availability check."""
        appointment_id = request.data.get('appointment_id')
        new_date = request.data.get('appointment_date')
        new_start_time = request.data.get('start_time')
        new_end_time = request.data.get('end_time')

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        if profile.role not in ['nurse', 'doctor']:
            return Response({'error': 'Only nurses and doctors can reschedule appointments'}, status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        doctor = appointment.doctor
        # Validate the new slot is within doctor's availability
        try:
            import datetime
            d = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
            day_map = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            day_code = day_map[d.weekday()]
        except Exception:
            return Response({'error': 'Invalid date format, use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        # Check doctor's availability slots
        if not DoctorAvailability.objects.filter(
            doctor=doctor,
            day_of_week=day_code,
            start_time__lte=new_start_time,
            end_time__gte=new_end_time,
            is_active=True
        ).exists():
            return Response({'error': 'New time is outside doctor\'s availability'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for conflicts
        conflicting = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=new_date,
            start_time__lt=new_end_time,
            end_time__gt=new_start_time,
            status='scheduled'
        ).exclude(id=appointment_id).exists()

        if conflicting:
            return Response({'error': 'New time slot conflicts with another appointment'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.appointment_date = new_date
        appointment.start_time = new_start_time
        appointment.end_time = new_end_time
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response({'message': 'Appointment rescheduled successfully', 'appointment': serializer.data}, status=status.HTTP_200_OK)
    
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
    permission_classes = [IsAuthenticated, IsReportAuthorOrNurseOrReadOnly]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        # If doctor, return reports for patients the doctor has seen; nurses can see all; patients see their own
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
        elif profile.role == 'nurse':
            # Nurses can see all reports
            return MedicalReport.objects.all()
        else:
            # patient: only their own reports
            return MedicalReport.objects.filter(patient=user)

    def perform_create(self, serializer):
        # Allow doctor's user to attach their Doctor record; allow nurse to attach Nurse record
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'doctor':
                try:
                    doctor = Doctor.objects.get(user=user)
                    serializer.save(doctor=doctor)
                except Doctor.DoesNotExist:
                    serializer.save()
            elif profile.role == 'nurse':
                try:
                    nurse = Nurse.objects.get(user=user)
                    serializer.save(nurse=nurse)
                except Nurse.DoesNotExist:
                    serializer.save()
            else:
                serializer.save()
        except UserProfile.DoesNotExist:
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


class NurseViewSet(viewsets.ModelViewSet):
    """ViewSet for nurse management (admin only)"""
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Nurses can only see themselves
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'nurse':
                return Nurse.objects.filter(user=user)
        except UserProfile.DoesNotExist:
            pass
        return Nurse.objects.none()


class AppointmentRescheduleViewSet(viewsets.ViewSet):
    """ViewSet for rescheduling appointments (nurse can reschedule)"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def reschedule(self, request):
        """Reschedule an appointment to a new date/time"""
        appointment_id = request.data.get('appointment_id')
        new_date = request.data.get('appointment_date')
        new_start_time = request.data.get('start_time')
        new_end_time = request.data.get('end_time')

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        # Only nurses and doctors can reschedule
        if profile.role not in ['nurse', 'doctor']:
            return Response({'error': 'Only nurses and doctors can reschedule appointments'}, 
                          status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Validate the appointment is available (no collision) and within doctor's schedule
        try:
            doctor = appointment.doctor
            # Check for conflicts
            conflicting = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=new_date,
                start_time__lt=new_end_time,
                end_time__gt=new_start_time,
                status='scheduled'
            ).exclude(id=appointment_id).exists()

            if conflicting:
                return Response({'error': 'New time slot conflicts with another appointment'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            appointment.appointment_date = new_date
            appointment.start_time = new_start_time
            appointment.end_time = new_end_time
            appointment.save()

            serializer = AppointmentSerializer(appointment)
            return Response({
                'message': 'Appointment rescheduled successfully',
                'appointment': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error rescheduling appointment: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset to fetch user profiles (for doctor patient lookups)"""
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # limit access: doctors and nurses can view profiles; patients can view only themselves
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return UserProfile.objects.none()

        if profile.role in ['doctor', 'nurse']:
            return self.queryset
        return UserProfile.objects.filter(user=user)

