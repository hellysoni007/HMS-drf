import datetime

from rest_framework import status
from rest_framework.response import Response
from .tasks import email_service

from account.models import User
from account.queries import get_user_from_id
from billing.models import SURGERY_CHARGE, ADMISSION_CHARGE, Bill
from billing.serializers import CreateBillSerializer

from operation.models import Operation, Admission
from patients.models import Appointment


class ManageBills:

    @staticmethod
    def new_bill_create_opd(request):
        """
        description: Logic for generating bill for opd
        params: Data(request)
        output: Response(Success or error msg)
        """
        opd_charges = 0
        total = 0
        bill_details = {}
        serializer = CreateBillSerializer(data=request.data)
        if request.data:
            patient = request.data['patient']
            today = datetime.date.today()
            user = get_user_from_id(patient)
            if not user:
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
            bill_created = serializer.save(opd_charge=opd_charges, total_charge=total, bill_details=bill_details)
            mail_body = "Bill details: " + '\n' + f'Bill Date: {datetime.date.today()}\nBill Id : {bill_created.id}\n' \
                                                  f'Bed charge : ' \
                                                  f'{bill_created.bed_charge}\nSurgery Charge : ' \
                                                  f'{bill_created.surgery_charge}\nAdmission ' \
                                                  f'Charge : {bill_created.admission_charge}\nOPD Charge : ' \
                                                  f'{bill_created.opd_charge}\nTotal : {bill_created.total_charge}'
            email_service.delay([bill_created.patient.email], "Your today's bill", mail_body)
            return Response({'msg': 'Bill generated Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def new_bill_create_operation(request):
        """
        description: Logic for generating bill for operations
        params: Data(request)
        output: Response(Success or error msg)
        """
        surgery_charge = 0
        admission_charge = 0
        bed_charge = 0
        total = 0
        bill_details = {}
        serializer = CreateBillSerializer(data=request.data)
        if request.data:
            patient = request.data['patient']
            today = datetime.date.today()
            user = get_user_from_id(patient)
            if not user:
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
            bill_created = serializer.save(surgery_charge=surgery_charge, admission_charge=admission_charge,
                                           bed_charge=bed_charge,
                                           total_charge=total,
                                           bill_details=bill_details)
            mail_body = "Bill details: " + '\n' + f'Bill Date: {datetime.date.today()}\nBill Id : {bill_created.id}\n' \
                                                  f'Bed charge : ' \
                                                  f'{bill_created.bed_charge}\nSurgery Charge : ' \
                                                  f'{bill_created.surgery_charge}\nAdmission ' \
                                                  f'Charge : {bill_created.admission_charge}\nOPD Charge : ' \
                                                  f'{bill_created.opd_charge}\nTotal : {bill_created.total_charge}'
            email_service.delay([bill_created.patient.email], "Your today's bill", mail_body)
            return Response({'msg': 'Bill generated Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagePrintingBills:
    @staticmethod
    def print_patient_bill(kwargs):
        """
                description: Logic for displaying particular patients bills
                params: kwargs(patient_id)
                output: Response(Data or error msg)
                """
        patient = kwargs['patient_id']
        queryset = Bill.objects.filter(patient=patient).order_by('-date')
        serializer = CreateBillSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def print_today_bills():
        """
                description: Logic for displaying today's bills
                params: None
                output: Response(Data or error msg)
                """
        today = datetime.date.today()
        queryset = Bill.objects.filter(date=today)
        serializer = CreateBillSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def print_bill_detail(kwargs):
        """
        description: Logic for displaying particular bill
        params: kwargs(bill_id)
        output: Response(Data or error msg)
        """
        bill_id = kwargs['bill_id']
        try:
            queryset = Bill.objects.get(id=bill_id)
        except Bill.DoesNotExist:
            return Response({'msg': 'Bill does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateBillSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
