from django.conf import settings
from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    legal_address = models.TextField()
    physical_address = models.TextField()


class Doctor(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=255)
    clinics = models.ManyToManyField(to="Clinic", related_name="doctors")

    @property
    def full_name(self):
        return self.user.get_full_name()


class Patient(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    @property
    def full_name(self):
        return self.user.get_full_name()


class Consultation(models.Model):
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('COMPLETED', 'Completed'),
        ('PAID', 'Paid'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    doctor = models.ForeignKey(to="Doctor", on_delete=models.CASCADE, related_name="consultations")
    patient = models.ForeignKey(to="Patient", on_delete=models.CASCADE, related_name="consultations")
    clinic = models.ForeignKey(to="Clinic", on_delete=models.CASCADE, related_name="consultations")
