from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json

from .models import Service, Appointment, Employee, TimeSlot, Notification
from .forms import ServiceForm,AppointmentForm, EmployeeForm, TimeSlotForm, NotificationForm

# Create your views here.

class HomeView(TemplateView):
    template_name = 'booking/home.html'

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    context_object_name = 'services'

class ServiceCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service-list')
    permission_required = 'booking.add_service'
    context_object_name = 'service'

class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service-list')
    permission_required = 'booking.change'
    context_object_name = 'service'

class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('service-list')
    permission_required = 'booking.delete'
    context_object_name = 'service'

class TimeSlotListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    context_object_name = 'timeslots'

class TimeSlotCreateView(PermissionRequiredMixin, CreateView):
    model = TimeSlot
    form_class = TimeSlotForm
    success_url = reverse_lazy('timeslot-list')
    permission_required = 'booking.add-timeslot'
    context_object_name = 'timeslot'

class TimeSlotUpdateView(PermissionRequiredMixin, UpdateView):
    model = TimeSlot
    form_class = TimeSlotForm
    success_url = reverse_lazy('timeslot-list')
    permission_required = 'booking.change_timeslot'
    context_object_name = 'timeslot'

class TimeSlotDeleteView(PermissionRequiredMixin, DeleteView):
    model = TimeSlot
    success_url = reverse_lazy('timeslot-list')
    permission_required = 'booking.delete_timeslot'
    context_object_name = 'timeslot'

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'

    def qet_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif hasattr(user, 'employee'):
            return Appointment.objects.filter(employee=user.employee)
        return Appointment.objects.filter(customer=user)
    
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment-list')
    context_object_name = 'appointment'

    def form_valid(self, form):
        user = self.request.user
        if not user.is_staff and not hasattr(user, 'employee'):
            form.instance.customer = user
        return super().form_valid(form)
    
class AppointmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment-list')
    permission_required = 'booking.change-appointment'
    context_object_name = 'appointmen'

class AppointmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment-lazy')
    permission_required = 'booking.delete_appointment'
    context_object_name = 'appointment'
    

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'booking.add_employee'
    context_object_name = 'employee'

    def test_func(self):
        return self.request.user.is_staff
    
class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Employee
    context_object_name = 'employees'

    def get_queryset(self):
        return self.models.objects.filter(user=self.request.user).order_by()
    
# class EmployeeDetailView(LoginRequiredMixin, DetailView):
#     model = Employee
#     template_name = 'booking/employee_details.html'
#     context_object_name = 'employees'

#     def get_queryset(self):
#         return self.models.objects.filter(user=self.request.user).order_by()
 
class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
     model = Employee
     form_class = EmployeeForm
     success_url = reverse_lazy('employee_list')
     permission_required = 'booking.change_employee'
     context_object_name = 'employee'

     def test_func(self):
        return self.request.user.is_staff
     
   
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee-list')
    permission_required = 'booking.delete_employee'
    context_object_name = 'employee'

    def get_queryset(self):
        return self.models.objectss.filter(user=self.request.user).order_by()
    

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notification-list'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or hasattr(user, 'employee'):
            return Notification.objects.all()
        return Notification.objects.filter(user=user)
    
class NotificationCreateView(PermissionRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    success_url = reverse_lazy('notification-list')
    permission_required = 'booking.add_notification'
    context_object_name = 'notification'

class NotificationUpdateView(PermissionRequiredMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    success_url = reverse_lazy('notification-list')
    permission_required = 'booking.change_notification'
    context_object_name = 'notification'

class NotificationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Notification
    success_url = reverse_lazy('notification-list')
    permission_required = 'booking.delete_notification'
    context_object_name = 'notification'




class CalendarView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'appointments/calendar.html'
    permission_required = 'appointments.view_appointment'

def appointment_events(request):
    user = request.user
    if user.has_perm('appointments.view_appointment'):
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(user=user)

    events = []
    for a in appointments:
        events.append({
            'title': f'{a.service.name} with {a.employee.name}',
            'start': f'{a.timeslot.date}T{a.timeslot.start_time}',
            'end': f'{a.timeslot.date}T{a.timeslot.end_time}',
            'url': f'/appointments/{a.id}/edit/',
            'color': '#3498db' if a.status=='confirmed' else '#e67e22',
        })
    return JsonResponse(events, safe=False)

class AppointmentCreateAjax(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form_partial.html'
    permission_required = 'appointments.add_appointment'

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        if date:
            initial['timeslot_date'] = date
        return initial

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True, 'redirect': True})

class AppointmentUpdateAjax(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form_partial.html'
    permission_required = 'appointments.change_appointment'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True, 'redirect': True})