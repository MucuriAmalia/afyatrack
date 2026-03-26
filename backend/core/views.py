from django.shortcuts import render, redirect
from .forms import HouseholdForm
from .models import Household
from django.http import JsonResponse
from core.models import SubCounty, Ward
from core.forms import PatientForm, AppointmentForm, PatientRecordForm
from core.models import Patient, Appointment, Clinic, PatientRecord
from django.utils import timezone


def register_household(request):

    if request.method == "POST":
        form = HouseholdForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("household_list")

    else:
        form = HouseholdForm()

    return render(request, "core/register_household.html", {"form": form})


def household_list(request):

    households = Household.objects.all().order_by("-created_at")

    return render(
        request,
        "core/household_list.html",
        {"households": households},
    )

def load_subcounties(request):
    county_id = request.GET.get('county')
    subcounties = SubCounty.objects.filter(county_id=county_id).order_by('name')
    return JsonResponse(list(subcounties.values('id', 'name')), safe=False)

def load_wards(request):
    subcounty_id = request.GET.get('subcounty')
    wards = Ward.objects.filter(subcounty_id=subcounty_id).order_by('name')
    return JsonResponse(list(wards.values('id', 'name')), safe=False)


# --- Patient ---
def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'core/register_patient.html', {'form': form})

def patient_list(request):
    patients = Patient.objects.select_related('household').all()
    return render(request, 'core/patient_list.html', {'patients': patients})


# --- Appointment ---
def register_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'core/register_appointment.html', {'form': form})

def appointment_list(request):
    appointments = Appointment.objects.select_related('patient','clinic').all()
    return render(request, 'core/appointment_list.html', {'appointments': appointments})


# --- Patient Record / EMR ---
def add_patient_record(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.appointment = appointment
            record.save()
            return redirect('appointment_list')
    else:
        form = PatientRecordForm()
    return render(request, 'core/add_patient_record.html', {'form': form, 'appointment': appointment})