import datetime

from django.db import models

from account.models import User

today = datetime.date.today()

BLOODGROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
               ('O-', 'O-'), ('NA', 'NA')]

PROCEDURE = [('Appointment', 'Appointment'), ('Operation', 'Operation'), ('Admitted', 'Admitted'),
             ('Discharged', 'Discharged'), ('Reports', 'Reports'), ('Registered', 'Registered')]


class Procedure(models.Model):
    name = models.CharField(
        max_length=11,
        choices=PROCEDURE,
        default='NA'
    )
    status = models.CharField(
        max_length=20
    )


class PatientProfile(models.Model):
    patient_id = models.ForeignKey(User, related_name='patient_profile', on_delete=models.CASCADE)
    blood_group = models.CharField(
        max_length=3,
        choices=BLOODGROUPS,
        default='NA'
    )
    disease = models.CharField(max_length=50, blank=True)
    advised_procedure = models.ForeignKey(Procedure, related_name='current_process', on_delete=models.CASCADE,
                                          blank=True, null=True)
    has_allergies = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    has_medical_history = models.BooleanField(default=False)
    medical_history = models.TextField(blank=True)


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
