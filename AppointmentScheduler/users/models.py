from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    user_id = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.username