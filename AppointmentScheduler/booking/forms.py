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
        fields = ['employee', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class EmployeeForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'specialization', 'email', 'phone_number', 'years_experience', 'bio', 'is_active']

class AppointmentForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['employee', 'services', 'appointment_date', 'timeslot', 'status', 'notes']
        widgets = {
             'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_date'].required = False
        # Filter to show only unbooked timeslots, plus the current one if we are editing
        if self.instance and self.instance.pk and self.instance.timeslot:
            self.fields['timeslot'].queryset = TimeSlot.objects.filter(models.Q(is_booked=False) | models.Q(pk=self.instance.timeslot.pk))
        elif 'timeslot' in self.data:
            try:
                timeslot_id = int(self.data.get('timeslot'))
                self.fields['timeslot'].queryset = TimeSlot.objects.filter(models.Q(is_booked=False) | models.Q(pk=timeslot_id))
            except (ValueError, TypeError):
                self.fields['timeslot'].queryset = TimeSlot.objects.filter(is_booked=False)
        else:
             self.fields['timeslot'].queryset = TimeSlot.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        timeslot = cleaned_data.get('timeslot')
        appointment_date = cleaned_data.get('appointment_date')

        if timeslot:
            # If a timeslot is selected, override appointment_date with timeslot's datetime
            import datetime
            # Combine date and time
            dt = datetime.datetime.combine(timeslot.date, timeslot.start_time)
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            cleaned_data['appointment_date'] = dt
            
            # Check availability (redundant but safe)
            if timeslot.is_booked:
                # Allow if editing the same instance
                if self.instance and self.instance.timeslot == timeslot:
                    pass
                else:
                    self.add_error('timeslot', "This time slot has already been booked.")
        elif not appointment_date:
             self.add_error('appointment_date', "Please select a time slot OR enter a manual date/time.")
        
        return cleaned_data
        
class NotificationForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Notification
        fields =['recipient', 'message', 'is_read']