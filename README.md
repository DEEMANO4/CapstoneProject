Appointment Scheduler App (Django)
📌 Overview

The Appointment Scheduler App is a web-based application built with Django that allows users to easily schedule appointments using an interactive calendar. Users can choose the service they need, select a preferred employee, view available time slots, and receive notifications related to their appointments.

The application is designed with scalability and clarity in mind, using Django’s class-based views, authentication system, permissions, and a clean project structure.

🚀 Features

User Authentication

Custom user model

Secure login and logout

Permission-based access control

Appointment Scheduling

Schedule appointments through a calendar interface

View appointments in a calendar layout

Edit or cancel appointments

Employee Selection

Choose a specific employee when booking an appointment

Each employee has their own available time slots

Time Slot Management

View available time slots before booking

Prevent double booking

Mark time slots as available or unavailable

Services Management

Appointments are linked to specific services

Each service includes duration and pricing information

Notifications

Users receive notifications for scheduled appointments

Notifications are linked to appointment events

Supports read/unread status

Permissions & Security

Uses LoginRequiredMixin and PermissionRequiredMixin

Only authorized users can create, update, or delete data

Admin Dashboard

Full CRUD management for users, services, employees, time slots, appointments, and notifications

🛠️ Technologies Used

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite (default, easily switchable)

Calendar Integration: JavaScript-based calendar (e.g., FullCalendar)

Authentication: Django Authentication System

Permissions: Django Permissions Framework

📂 Project Structure (Simplified)
mAppointmentScheduler/
├── users/            # Custom user app
├── booking/     # Core appointment scheduler logic
├── templates/        # HTML templates
├── static/           # CSS
├── manage.py
└── README.md

⚙️ Setup Instructions

Clone the repository

git clone <repository-url>
cd CapstoneProject


Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


Install dependencies

pip install django


Run migrations

python manage.py makemigrations
python manage.py migrate


Create a superuser

python manage.py createsuperuser


Start the development server

python manage.py runserver


Access the app

App: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

📅 How the Appointment Flow Works

User logs in

User opens the calendar view

User selects a date

User chooses:

Service

Preferred employee

Available time slot

Appointment is created

Notification is generated for the appointment

📈 Future Improvements

Email and SMS notifications

Employee working hours configuration

Recurring appointments

Payment integration

REST API for mobile support

👨‍💻 Author

MANO
