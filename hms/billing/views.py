import datetime

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from account.models import User
from account.permissions import IsReceptionist, IsAdmin
from billing.serializers import CreateBillSerializer
from operation.models import Operation, Admission
from patients.models import Appointment

from .models import ADMISSION_CHARGE, SURGERY_CHARGE, Bill
from .services import ManageBills


class GenerateOPDBillView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        params: patient_id,operation_id,opd_id
        """
        new_bill = ManageBills.new_bill_create_opd(request)
        return new_bill


class GenerateOperationBillView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        params: patient_id,operation_id,opd_id
        """
        new_bill = ManageBills.new_bill_create_operation(request)
        return new_bill


class PrintPatientBillView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        patient = kwargs['patient_id']
        queryset = Bill.objects.filter(patient=patient).order_by('-date')
        serializer = CreateBillSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodayBillsView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        queryset = Bill.objects.filter(date=today)
        serializer = CreateBillSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BillDetailView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def get(self, request, *args, **kwargs):
        bill_id = kwargs['bill_id']
        try:
            queryset = Bill.objects.get(id=bill_id)
        except Bill.DoesNotExist:
            return Response({'msg': 'Bill does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateBillSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
