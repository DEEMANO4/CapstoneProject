from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

class Service(models.Model):
    service_id = models.IntegerField()
    service = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.IntegerField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=100)
    years_experience = models.IntegerField()
    bio = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='timeslots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.employee.name} - {self.date} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    appointment_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    services = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='services')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employees')
    # service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service id')
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timeslots_available' )
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} for {self.user.username} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"




# User = get_user_model

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('BOOKING_CONFIRMIATION', 'Booking Confirmation'),
        ('REMINDER', 'Reminder'),
        ('CANCELLATION', 'Cancellation'),
        ('RESCHEDULE', 'Reschedule'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.notification_type}"
    
