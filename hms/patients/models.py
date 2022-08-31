import datetime

from django.db import models

from account.models import User

today = datetime.date.today()

BLOODGROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
               ('O-', 'O-'), ('NA', 'NA')]

PROCEDURE = [('Operation', 'Operation'), ('Admitted', 'Admitted'), ('Medication', 'Medication'),
             ('Discharged', 'Discharged'), ('Reports', 'Reports')]


class Procedure(models.Model):
    name = models.CharField(
        max_length=50
    )


class PatientProfile(models.Model):
    patient_id = models.ForeignKey(User, related_name='patient_profile', on_delete=models.CASCADE)
    blood_group = models.CharField(
        max_length=3,
        choices=BLOODGROUPS,
        default='NA'
    )
    disease = models.CharField(max_length=50, blank=True)
    has_allergies = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    has_medical_history = models.BooleanField(default=False)
    medical_history = models.TextField(blank=True)
    advise = models.CharField(max_length=50, choices=PROCEDURE, default='NA')


class TimeSlots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()


STATUS = [('SCHEDULED', 'SCHEDULED'), ('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED')]


class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name='patient_id', on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(User, related_name='doctor_id', on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    timeslot = models.ForeignKey(TimeSlots, related_name='slot', on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=STATUS, max_length=10, default='SCHEDULED')


class Prescription(models.Model):
    patient = models.ForeignKey(User, related_name='prescription', on_delete=models.CASCADE, null=True)
    for_no_days = models.IntegerField(null=False, blank=False)
    date = models.DateField(auto_now_add=True, blank=True, null=True)


class Medication(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    brand = models.CharField(max_length=200, blank=False, null=False)
    dose_per_day = models.IntegerField(null=False, blank=False)
    how_to_consume = models.CharField(max_length=200, blank=False, null=False)
    prescription = models.ForeignKey(Prescription, related_name='Medication', on_delete=models.CASCADE, null=True)
