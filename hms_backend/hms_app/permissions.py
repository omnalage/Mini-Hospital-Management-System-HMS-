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
