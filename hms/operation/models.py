from django.db import models

from account.models import Rooms, User
from patients.models import TimeSlots


class Bed(models.Model):
    name = models.IntegerField()
    room = models.ForeignKey(Rooms, related_name='room', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True, blank=False, null=False)
    charges_per_day = models.IntegerField()
    is_delete = models.BooleanField(default=False)


class Admission(models.Model):
    patient = models.ForeignKey(User, related_name='admitted_patient', on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, related_name="allotted_bed", on_delete=models.CASCADE)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)


OPERATION_STATUS = [('SCHEDULED', 'SCHEDULED'), ('COMPLETED', 'COMPLETED')]


class Operation(models.Model):
    doctor = models.ForeignKey(User, related_name='operated_by', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='operated_patient', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, name="operation-name")
    date = models.DateField(null=False, blank=False)
    timeslot = models.ForeignKey(TimeSlots, related_name='timeslot', on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=OPERATION_STATUS, default='NA')
    instructions = models.CharField(max_length=50)
