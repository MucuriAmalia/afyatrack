from django.db import models
from core.models import Household

# --- Patient ---
class Patient(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('M','Male'),('F','Female')))
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# --- Clinic ---
class Clinic(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


# --- Appointment ---
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=(
        ('Pending','Pending'),
        ('In Consultation','In Consultation'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
    ), default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# --- Queue (optional, derived from today's appointments) ---
class Queue(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    checked_in = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)


# --- EMR / Patient Record ---
class PatientRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    vitals = models.JSONField(blank=True, null=True)  # {"BP":"120/80", "Temp":"37C"}
    diagnosis = models.TextField(blank=True, null=True)