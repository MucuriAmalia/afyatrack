from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "country")

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "county")

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "subcounty")

    def __str__(self):
        return self.name


class CommunityUnit(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "ward")

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100)
    community_unit = models.ForeignKey(CommunityUnit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "community_unit")

    def __str__(self):
        return self.name


class Household(models.Model):
    household_code = models.CharField(max_length=50, unique=True)
    head_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Location hierarchy
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)

    # Optional: GPS coordinates
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Optional: additional fields for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.household_code} - {self.head_name}"


class Patient(models.Model):

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )

    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    clinic = models.CharField(max_length=100)  # or a ForeignKey to Clinic if you have that model
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.scheduled_date} {self.scheduled_time}"


class PatientRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    vitals = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.appointment.patient} on {self.appointment.scheduled_date}"