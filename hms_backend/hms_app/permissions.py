from rest_framework import permissions
from .models import UserProfile, Doctor


class IsDoctorOrReadOnly(permissions.BasePermission):
    """Only doctors can edit doctor-related objects"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'doctor'
        except UserProfile.DoesNotExist:
            return False


class IsPatientOrReadOnly(permissions.BasePermission):
    """Only patients can book appointments"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'patient'
        except UserProfile.DoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allow users to manage their own objects"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user


class IsReportAuthorOrNurseOrReadOnly(permissions.BasePermission):
    """Allow safe methods for everyone. For edits, allow the doctor who authored the report or any nurse (or superuser)."""

    def has_object_permission(self, request, view, obj):
        # Safe methods allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superusers can do anything
        try:
            if request.user and request.user.is_superuser:
                return True
        except Exception:
            pass

        # Determine role
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return False

        # Nurses can edit
        if profile.role == 'nurse':
            return True

        # Doctors can edit only reports they authored
        if profile.role == 'doctor':
            try:
                return obj.doctor is not None and obj.doctor.user == request.user
            except Exception:
                return False

        return False
