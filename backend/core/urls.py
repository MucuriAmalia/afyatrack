from django.urls import path
from . import views

urlpatterns = [

    path("", views.household_list, name="household_list"),

    path(
        "households/register/",
        views.register_household,
        name="register_household"
    ),

    path('ajax/load-subcounties/', views.load_subcounties, name='ajax_load_subcounties'),
    path('ajax/load-wards/', views.load_wards, name='ajax_load_wards'),

    # Patients
    path('patients/register/', views.register_patient, name='register_patient'),
    path('patients/', views.patient_list, name='patient_list'),

    # Appointments
    path('appointments/register/', views.register_appointment, name='register_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),

    # Patient EMR
    path('appointments/<int:appointment_id>/record/', views.add_patient_record, name='add_patient_record'),

]