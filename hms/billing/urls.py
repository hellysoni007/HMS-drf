from django.urls import path

from billing.views import GenerateOPDBillView, GenerateOperationBillView, PrintPatientBillView, TodayBillsView, \
    BillDetailView

# from .views import

urlpatterns = [
    path('generate/OPD/', GenerateOPDBillView.as_view(), name="generate-bill-for-OPD"),
    path('generate/Operation/', GenerateOperationBillView.as_view(), name="generate-bill-for-operation"),
    path('<int:patient_id>', PrintPatientBillView.as_view(), name="get-all-bills-by-patient"),
    path('<int:patient_id>/<int:bill_id>', BillDetailView.as_view(), name="print-bill"),
    path('today/', TodayBillsView.as_view(), name="get-all-todays-bills"),
    path('today/<int:bill_id>', BillDetailView.as_view(), name="print-bill"),

]
