from django.urls import path
from . import views
from .views import (ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
                    TimeSlotListView, TimeSlotCreateView, TimeSlotUpdateView, TimeSlotDeleteView,
                    EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView,
                    AppointmentListView, AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView,
                    NotificationListView, NotificationCreateView, NotificationUpdateView, NotificationDeleteView)

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service/create/', ServiceCreateView.as_view(), name='service-create'),
    path('service/<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
    path('timeslots/', TimeSlotListView.as_view(), name='timeslots'),
    path('timeslots/create/', TimeSlotCreateView.as_view(), name='timeslots-create'),
    path('timeslots/<int:pk>/update/', TimeSlotUpdateView.as_view(), name='timeslots-update'),
    path('timeslots/<int:pk>/delete/', TimeSlotDeleteView.as_view(), name='timeslots-delete'),
    path('employee/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>?update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/create/', NotificationCreateView.as_view(), name='notification-create'),
    path('notifications/<int:pk>/update/', NotificationUpdateView.as_view(), name='notification-update'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification-delete'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/events/', views.appointment_events, name='calendar_events'),
    path('appointments/add/', views.AppointmentCreateAjax.as_view(), name='appointment_add'),
    path('appointments/<int:pk>/edit/', views.AppointmentUpdateAjax.as_view(), name='appointment_edit'),
]