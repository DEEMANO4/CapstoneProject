from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['user_id', 'username', 'email','password', 'first_name', 'last_name', 'phone_number', 'registration_date']

admin.site.register(CustomUser, CustomUserAdmin)