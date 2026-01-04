from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import json

from .models import Service, Appointment, Employee, TimeSlot, Notification
from .forms import ServiceForm,AppointmentForm, EmployeeForm, TimeSlotForm, NotificationForm

# Create your views here.

from django.db.models import Count, Sum
from django.utils import timezone

class HomeView(TemplateView):
    template_name = 'booking/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['total_appointments'] = Appointment.objects.count()
        context['upcoming_appointments'] = Appointment.objects.filter(appointment_date__gte=today).count()
        context['total_employees'] = Employee.objects.filter(is_active=True).count()
        
        revenue = Appointment.objects.filter(status='active').aggregate(
            total_revenue=Sum('services__price')
        )['total_revenue']
        context['total_revenue'] = revenue if revenue else 0
        
        return context

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    context_object_name = 'services'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(service__icontains=q)
        return queryset

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

    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.none()
        if user.is_staff:
            queryset = Appointment.objects.all()
        elif hasattr(user, 'employee'):
            queryset = Appointment.objects.filter(employee=user.employee)
        else:
            queryset = Appointment.objects.filter(user=user)
        
        q = self.request.GET.get('q')
        if q:
             queryset = queryset.filter(
                models.Q(services__service__icontains=q) | 
                models.Q(employee__name__icontains=q)
             )
        return queryset
    
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment-list')
    context_object_name = 'appointment'

    def form_valid(self, form):
        user = self.request.user
        # Automatically assign the logged-in user to the appointment
        form.instance.user = user
        response = super().form_valid(form)
        if self.object.timeslot:
            self.object.timeslot.is_booked = True
            self.object.timeslot.save()
        return response
    
class AppointmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('appointment-list')
    permission_required = 'booking.change-appointment'
    context_object_name = 'appointment'

class AppointmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment-list')
    permission_required = 'booking.delete_appointment'
    context_object_name = 'appointment'

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.timeslot:
             self.object.timeslot.is_booked = False
             self.object.timeslot.save()
        self.object.delete()
        return redirect(success_url)
    

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee-list')
    permission_required = 'booking.add_employee'
    context_object_name = 'employee'

    def test_func(self):
        return self.request.user.is_staff
    
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset
    
# class EmployeeDetailView(LoginRequiredMixin, DetailView):
#     model = Employee
#     template_name = 'booking/employee_details.html'
#     context_object_name = 'employees'

#     def get_queryset(self):
#         return self.models.objects.filter(user=self.request.user).order_by()
 
class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
     model = Employee
     form_class = EmployeeForm
     success_url = reverse_lazy('employee-list')
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
        return self.model.objects.filter(is_active=True)
    

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
    permission_required = 'booking.view_appointment'

def appointment_events(request):
    user = request.user
    if user.has_perm('booking.view_appointment'):
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(user=user)

    events = []
    for a in appointments:
        start_time = None
        end_time = None
        
        if a.timeslot:
            start_time = f'{a.timeslot.date}T{a.timeslot.start_time}'
            end_time = f'{a.timeslot.date}T{a.timeslot.end_time}'
        elif a.appointment_date:
            start_time = a.appointment_date.isoformat()
            # Default to 1 hour duration if no timeslot/duration available
            end_time = (a.appointment_date + __import__('datetime').timedelta(hours=1)).isoformat()
            
        if start_time and a.services and a.employee:
            events.append({
                'title': f'{a.services.service} with {a.employee.name}',
                'start': start_time,
                'end': end_time,
                'url': f'/appointments/appointments/{a.id}/update/',
                'color': '#3498db' if a.status=='active' else '#e67e22',
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