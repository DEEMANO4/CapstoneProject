from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json

from .models import Service, Appointment, Employee, TimeSlot, Notification

# Create your views here.

class HomeView(TemplateView):
    template_name = 'booking/home.html'

class ServiceListeView(ListView):
    model = Service
    template_name = 'booking/service_list.html'
    context_object_name = 'services'

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'booking/appointment_list.html'
    context_object_name = 'appointments'

    def qet_queryset(self):
        return Appointment.objects.filter(user=self.request.user).order_by('start_time')
    
class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'booking/appointment_details.html'
    context_object_name = 'appointment' 

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class AppointmentCancelView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'booking/cancel_appointment.html'
    success_url = reverse_lazy('booking:my_appointments')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ['service_offered', 'employee_available,', 'time_slot']
    template_name = 'booking/appoinment_booking.html' 
    success_url = reverse_lazy('booking:my_appointments')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time_slot.is_booked = True
        form.instance.time_slot.save()
        return super().form_valid(form)
    
class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['service_offered', 'employee_available,', 'time_slot']
    template_name = 'booking/appoinment_booking.html' 
    success_url = reverse_lazy('booking:my_appointments')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.time_slot.is_booked = True
        form.instance.time_slot.save()
        return super().form_valid(form)
    
def load_available_timeslots(request):
    employee_id = request.GET,get('emplyee_id')
    service_id = request.GET.get('service_id')

    timeslots = TimeSlot.objects.filter(employee_id=employee_id, is_booked= False, service_id=service_id).order_by('start_time')

    data = [{
        'id': time_slot.id,
        'start_time': time_slot.start_time.strftime('Y-%m-%d %H:%M'),
        'end_time': time_slot.end_time.strftime('%Y-%m-%d %H:%M'),
    } for time_slot in timeslots]

    return JsonResponse(data, safe=False)

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'booking/notification_list.html'
    context_object_name ='notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if request.method ==  'POST':
        notification.is_read = True
        notification.save()

        return redirect('booking:notification_list.html')
    

class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    fields = ['name', 'specialization']
    template_name = 'booking/employee_form.html'
    success_url = reverse_lazy('booking:employee_list')

    def test_func(self):
        return self.request.user.is_staff
    
class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Employee
    template_name = 'booking/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return self.models.objects.filter(user=self.request.user).order_by()
    
class EmployeeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Employee
    template_name = 'booking/employee_details.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return self.models.objects.filter(user=self.request.user).order_by()
    
class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'booking/employee_removed.html'
    success_url = reverse_lazy('booking:my_appointments')

    def get_queryset(self):
        return self.models.objectss.filter(user=self.request.user).order_by()
    
class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = Employee
     fields = ['name', 'specialization']
     template_name = 'booking/employee_form.html'
     success_url = reverse_lazy('booking:employee_list')

     def test_func(self):
        return self.request.user.is_staff