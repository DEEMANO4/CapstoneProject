from django import forms
from .models import Appointment, Service, Employee, TimeSlot, Notification
from django.db import models
from django.utils import timezone

   
class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600 ' + current_classes
            else:
                field.widget.attrs['class'] = 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 pl-2 ' + current_classes

class ServiceForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
         model = Service
         fields = ['service', 'price', 'duration']

class TimeSlotForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time', 'date']

class EmployeeForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'specialization', 'email', 'phone_number', 'years_experience', 'bio', 'is_active']

class AppointmentForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['employee', 'services', 'timeslot', 'appointment_date', 'status', 'notes']
        widgets = {
             'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only unbooked timeslots, plus the current one if we are editing
        if self.instance and self.instance.pk and self.instance.timeslot:
            self.fields['timeslot'].queryset = TimeSlot.objects.filter(models.Q(is_booked=False) | models.Q(pk=self.instance.timeslot.pk))
        else:
            self.fields['timeslot'].queryset = TimeSlot.objects.filter(is_booked=False)

    def clean_timeslot(self):
        timeslot = self.cleaned_data.get('timeslot')
        if timeslot and timeslot.is_booked:
            # Check if we are editing and this is our own timeslot
            if self.instance and self.instance.timeslot == timeslot:
                pass
            else:
                raise forms.ValidationError("This time slot has already been booked.")
        return timeslot
        
class NotificationForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Notification
        fields =['recipient', 'message', 'is_read']