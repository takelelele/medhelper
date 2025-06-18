from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrator'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )

    role = models.CharField(max_length=10, choices=ROLES)
    phone = models.CharField(max_length=20, blank=True, null=True)
