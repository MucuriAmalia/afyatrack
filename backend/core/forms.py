from django import forms
from .models import Household
from core.models import Patient, Appointment, PatientRecord



class HouseholdForm(forms.ModelForm):

    class Meta:
        model = Household
        fields = [
            "household_code",
            "head_name",
            "phone_number",
            "village",
            "latitude",
            "longitude",
        ]

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['household', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'clinic', 'scheduled_date', 'scheduled_time', 'status']

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['appointment', 'vitals', 'notes', 'diagnosis']