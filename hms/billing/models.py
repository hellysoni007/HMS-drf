from django.db import models

from account.models import User, Rooms

ADMISSION_CHARGE = 5000
SURGERY_CHARGE = 10000


# Create your models here.
class Bill(models.Model):
    patient = models.ForeignKey(User, related_name='bill_details', on_delete=models.CASCADE, null=False, blank=False)
    bed_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    surgery_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    admission_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    opd_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    bill_details = models.JSONField()
