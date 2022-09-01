from django.db import models

from account.models import Rooms


class Bed(models.Model):
    name = models.IntegerField()
    room = models.ForeignKey(Rooms, related_name='room', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True, blank=False, null=False)
    charges_per_day = models.IntegerField()

# class Admission(models.Model):
#     patient
#     bed
#     admission_date
#     discharge_date
#     pass
#
#
# class Operation(models.Model):
#     pass
