from rest_framework import generics

from account.permissions import IsReceptionist, IsAdmin
from .services import ManageBills, ManagePrintingBills


class GenerateOPDBillView(generics.CreateAPIView):
    """
    Generate bills for opd by receptionist
    """
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        description: Generating bill for OPD
        params: patient_id,operation_id,opd_id
        output: new bill generated msg
        """
        new_bill = ManageBills.new_bill_create_opd(request)
        return new_bill


class GenerateOperationBillView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        description: Generating bill for operation
        params: patient_id,operation_id,opd_id
        output: new bill generated msg
        """
        new_bill = ManageBills.new_bill_create_operation(request)
        return new_bill


class PrintPatientBillView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Get bill of the patient
        params: patient_id
        output: displays bill for the patient
        """
        print_bill = ManagePrintingBills.print_patient_bill(kwargs)
        return print_bill


class TodayBillsView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: Get all todays bills
        params: None
        output: displays all todays bills
        """
        print_bill = ManagePrintingBills.print_today_bills()
        return print_bill


class BillDetailView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: Get bill details
        params: bill_id
        output: displays all bill details
        """
        print_bill = ManagePrintingBills.print_bill_detail(kwargs)
        return print_bill
