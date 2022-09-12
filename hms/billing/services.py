import datetime

from rest_framework import status
from rest_framework.response import Response

from account.models import User
from billing.models import SURGERY_CHARGE, ADMISSION_CHARGE
from billing.serializers import CreateBillSerializer
from operation.models import Operation, Admission
from patients.models import Appointment


class ManageBills:

    @staticmethod
    def new_bill_create_opd(request):
        opd_charges = 0
        total = 0
        bill_details = {}
        serializer = CreateBillSerializer(data=request.data)
        if request.data:
            patient = request.data['patient']
            today = datetime.date.today()
            try:
                patient_obj = User.objects.get(id=patient)
            except User.DoesNotExist:
                return Response({'error-msg': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND)
            try:
                appointment = Appointment.objects.get(patient=patient, status="COMPLETED", date=today)
            except Appointment.DoesNotExist:
                return Response({'error-msg': 'Patient does not have any OPD or OPD is not yet completed'},
                                status=status.HTTP_404_NOT_FOUND)
            bill_details = {
                'opd_id': appointment.id
            }
            opd_charges = 500
            total = opd_charges
        if serializer.is_valid(raise_exception=True):
            serializer.save(opd_charge=opd_charges, total_charge=total, bill_details=bill_details)
            return Response({'msg': 'Bill generated Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def new_bill_create_operation(request):
        surgery_charge = 0
        admission_charge = 0
        bed_charge = 0
        total = 0
        bill_details = {}
        serializer = CreateBillSerializer(data=request.data)
        if request.data:
            patient = request.data['patient']
            today = datetime.date.today()
            try:
                patient_obj = User.objects.get(id=patient)
            except User.DoesNotExist:
                return Response({'error-msg': 'Patient does not exist'}, status=status.HTTP_404_NOT_FOUND)
            try:
                operation = Operation.objects.get(patient=patient, status="COMPLETED", date__lte=today)
                surgery_charge = SURGERY_CHARGE
            except Operation.DoesNotExist:
                return Response({'error-msg': 'Patient has not undergone any operations'},
                                status=status.HTTP_404_NOT_FOUND)
            try:
                admission = Admission.objects.get(patient=patient, discharge_date=today)
                charge = admission.bed.charges_per_day
                no_of_days = admission.discharge_date - admission.admission_date
                days = no_of_days.days
                bed_charge = days * charge
                admission_charge = ADMISSION_CHARGE
            except Admission.DoesNotExist:
                return Response({'error-msg': 'Patient has not been admitted'}, status=status.HTTP_404_NOT_FOUND)

            bill_details = {
                'operation_id': operation.id,
                'admission_id': admission.id
            }
            total = surgery_charge + admission_charge + bed_charge
        if serializer.is_valid(raise_exception=True):
            serializer.save(surgery_charge=surgery_charge, admission_charge=admission_charge, bed_charge=bed_charge,
                            total_charge=total,
                            bill_details=bill_details)
            return Response({'msg': 'Bill generated Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
