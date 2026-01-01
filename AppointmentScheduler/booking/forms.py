from django import forms
from .models import Appointment, Service, Employee, TimeSlot, Notification
from django.utils import timezone

   
class ServiceForm(forms.ModelForm):
    class Meta:
         model = Service
         fields = ['service', 'price']

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'specialization', 'is_active']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['user', 'employee', 'services', 'timeslot']
        
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields =['recipient', 'message', 'is_read']