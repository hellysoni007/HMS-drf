import pytest
from django.urls import reverse, resolve

import billing


@pytest.mark.django_db
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_generate_bill_for_opd_url(api_client):
    url = reverse("generate-bill-for-OPD")
    assert resolve(url).func.view_class == billing.views.GenerateOPDBillView


@pytest.mark.django_db
def test_generate_bill_for_operation_url(api_client):
    url = reverse("generate-bill-for-operation")
    assert resolve(url).func.view_class == billing.views.GenerateOperationBillView


@pytest.mark.django_db
def test_get_all_bills_by_patient_url(api_client):
    url = reverse("get-all-bills-by-patient", kwargs={'patient_id': 2})
    assert resolve(url).func.view_class == billing.views.PrintPatientBillView


@pytest.mark.django_db
def test_print_bill_url(api_client):
    url = reverse("print-bill", kwargs={'patient_id': 2, 'bill_id': 1})
    assert resolve(url).func.view_class == billing.views.BillDetailView


@pytest.mark.django_db
def test_get_all_todays_bills_url(api_client):
    url = reverse("get-all-todays-bills")
    assert resolve(url).func.view_class == billing.views.TodayBillsView


@pytest.mark.django_db
def test_print_today_bill_details_url(api_client):
    url = reverse("print-today-bill-details", kwargs={'bill_id': 1})
    assert resolve(url).func.view_class == billing.views.BillDetailView
