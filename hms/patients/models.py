import datetime

from django.db import models

from account.models import User

today = datetime.date.today()

BLOODGROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
               ('O-', 'O-'), ('NA', 'NA')]

PROCEDURE = [('Appointment', 'Appointment'), ('Operation', 'Operation'), ('Admitted', 'Admitted'),
             ('Discharged', 'Discharged'), ('Reports', 'Reports'), ('Registered', 'Registered')]

# timeslots = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
#                ('8', '8'), ('9', '9')]
timeslots = []
for i in range(1, 33):
    timeslots = timeslots + [(str(i), str(i))]


# Create your models here.

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
    patient_id = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
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

#
# class Appointment(models.Model):
#     patient = models.ManyToManyField(User, related_name='patient_id')
#     doctor = models.ManyToManyField(User, related_name='doctor_id')
#     date = models.DateField(null=True)
#     timeslot = models.CharField(max_length=2, choices=timeslots, default="1")
