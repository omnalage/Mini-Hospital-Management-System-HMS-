from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile


class HomeView(TemplateView):
    """Home page with login/signup"""
    template_name = 'auth/login_signup.html'


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    """Doctor dashboard page"""
    template_name = 'dashboard/doctor.html'
    login_url = '/'
    
    def get(self, request, *args, **kwargs):
        # Check if user is a doctor
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != 'doctor':
                return redirect('/')
        except UserProfile.DoesNotExist:
            return redirect('/')
        
        return super().get(request, *args, **kwargs)


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    """Patient dashboard page"""
    template_name = 'dashboard/patient.html'
    login_url = '/'
    
    def get(self, request, *args, **kwargs):
        # Check if user is a patient
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != 'patient':
                return redirect('/')
        except UserProfile.DoesNotExist:
            return redirect('/')
        
        return super().get(request, *args, **kwargs)


class NurseDashboardView(LoginRequiredMixin, TemplateView):
    """Nurse dashboard page"""
    template_name = 'dashboard/nurse.html'
    login_url = '/'
    
    def get(self, request, *args, **kwargs):
        # Check if user is a nurse
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role != 'nurse':
                return redirect('/')
        except UserProfile.DoesNotExist:
            return redirect('/')
        
        return super().get(request, *args, **kwargs)