import pytest
from django.urls import reverse, resolve

import operation
import patients


@pytest.mark.django_db
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_view_all_operations_url(api_client):
    url = reverse("view-all-operations")
    assert resolve(url).func.view_class == operation.views.ShowOperationsView


@pytest.mark.django_db
def test_update_operations_detail_url(api_client):
    url = reverse("update-operations-detail", kwargs={'op_id': 1})
    assert resolve(url).func.view_class == operation.views.UpdateOperationDetailView


@pytest.mark.django_db
def test_view_todays_operations_url(api_client):
    url = reverse("view-todays-operations")
    assert resolve(url).func.view_class == operation.views.ShowTodayOperationView


@pytest.mark.django_db
def test_view_doctors_operations_url(api_client):
    url = reverse("view-doctors-operations", kwargs={'doctor_id': 1})
    assert resolve(url).func.view_class == operation.views.ShowDoctorOperationView


@pytest.mark.django_db
def test_view_doctors_operations_today_url(api_client):
    url = reverse("view-doctors-operations-today", kwargs={'doctor_id': 1})
    assert resolve(url).func.view_class == operation.views.ShowTodayDoctorOperationView


@pytest.mark.django_db
def test_view_my_operations_url(api_client):
    url = reverse("view-my-operations")
    assert resolve(url).func.view_class == operation.views.ShowDoctorListOperationView


@pytest.mark.django_db
def test_view_my_operations_today_url(api_client):
    url = reverse("view-my-operations-today")
    assert resolve(url).func.view_class == operation.views.ShowDoctorListOperationTodayView


@pytest.mark.django_db
def test_show_patients_url(api_client):
    url = reverse("show-patients")
    assert resolve(url).func.view_class == patients.views.ShowRegisteredPatientView


@pytest.mark.django_db
def test_show_patients_details_url(api_client):
    url = reverse("show-patients", kwargs={'pk': 1})
    assert resolve(url).func.view_class == patients.views.ShowRegisteredPatientView


@pytest.mark.django_db
def test_schedule_operation_url(api_client):
    url = reverse("schedule-operation",kwargs={'patient_id':1})
    assert resolve(url).func.view_class == operation.views.ScheduleOperationView


@pytest.mark.django_db
def test_view_available_surgeons_url(api_client):
    url = reverse("view-available-surgeons")
    assert resolve(url).func.view_class == operation.views.DisplayAvailableSurgeons


@pytest.mark.django_db
def test_view_all_beds_url(api_client):
    url = reverse("view-all-beds")
    assert resolve(url).func.view_class == operation.views.DisplayBedsView


@pytest.mark.django_db
def test_add_bed_url(api_client):
    url = reverse("add-bed")
    assert resolve(url).func.view_class == operation.views.CreateUpdateBedView


@pytest.mark.django_db
def test_update_bed_url(api_client):
    url = reverse("update-bed", kwargs={'id': 1})
    assert resolve(url).func.view_class == operation.views.CreateUpdateBedView


@pytest.mark.django_db
def test_update_bed_availability_url(api_client):
    url = reverse("update-bed-availability", kwargs={'id': 2})
    assert resolve(url).func.view_class == operation.views.UpdateBedAvailabilityView


@pytest.mark.django_db
def test_delete_bed_url(api_client):
    url = reverse("delete-bed", kwargs={'id': 2})
    assert resolve(url).func.view_class == operation.views.DeleteBedView


@pytest.mark.django_db
def test_view_beds_detail_url(api_client):
    url = reverse("view-beds-detail", kwargs={'id': 2})
    assert resolve(url).func.view_class == operation.views.DisplayBedsView


@pytest.mark.django_db
def test_view_available_beds_url(api_client):
    url = reverse("view-available-beds")
    assert resolve(url).func.view_class == operation.views.DisplayAvailableBedsView


@pytest.mark.django_db
def test_view_available_timeslots_url(api_client):
    url = reverse("view-available-timeslots")
    assert resolve(url).func.view_class == operation.views.DisplayAvailableOTTimeslots


@pytest.mark.django_db
def test_create_admit_patient_url(api_client):
    url = reverse("create-admit-patient")
    assert resolve(url).func.view_class == operation.views.CreatePatientAdmissionDetailsView


@pytest.mark.django_db
def test_view_admissions_detail_url(api_client):
    url = reverse("view-admissions-detail", kwargs={'admission_id': 1})
    assert resolve(url).func.view_class == operation.views.ShowPatientAdmissionDetailsView


@pytest.mark.django_db
def test_update_admit_patient_discharge_date_url(api_client):
    url = reverse("update-admit-patient-discharge-date", kwargs={'admission_id': 1})
    assert resolve(url).func.view_class == operation.views.UpdatePatientAdmissionDetailsView


@pytest.mark.django_db
def test_view_all_admissions_url(api_client):
    url = reverse("view-all-admissions")
    assert resolve(url).func.view_class == operation.views.DisplayAllAdmittedPatientsView


@pytest.mark.django_db
def test_view_active_admissions_url(api_client):
    url = reverse("view-active-admissions")
    assert resolve(url).func.view_class == operation.views.DisplayCurrentlyAdmittedPatientsView


@pytest.mark.django_db
def test_view_patients_op_scheduled_url(api_client):
    url = reverse("view-patients-Op-scheduled")
    assert resolve(url).func.view_class == operation.views.DisplayScheduledPatientOperationView


@pytest.mark.django_db
def test_view_patients_op_scheduled_details_url(api_client):
    url = reverse("view-patients-Op-scheduled-details", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == operation.views.DisplayScheduledPatientOperationView


@pytest.mark.django_db
def test_view_patients_op_all_url(api_client):
    url = reverse("view-patients-Op-all")
    assert resolve(url).func.view_class == operation.views.DisplayAllPatientOperationView


@pytest.mark.django_db
def test_view_patients_op_all_details_url(api_client):
    url = reverse("view-patients-Op-all-details", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == operation.views.DisplayAllPatientOperationView


@pytest.mark.django_db
def test_view_post_op_visits_url(api_client):
    url = reverse("view-post-op-visits", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == operation.views.PatientVisitView


@pytest.mark.django_db
def test_show_nurse_visit_details_url(api_client):
    url = reverse("show-nurse-visit-details")
    assert resolve(url).func.view_class == operation.views.CreateNurseVisitView


@pytest.mark.django_db
def test_add_nurse_visit_details_url(api_client):
    url = reverse("add-nurse-visit-details", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == operation.views.CreateNurseVisitView


@pytest.mark.django_db
def test_show_visit_details_url(api_client):
    url = reverse("show-visit-details")
    assert resolve(url).func.view_class == operation.views.CreateDoctorVisitView


@pytest.mark.django_db
def test_add_visit_details_url(api_client):
    url = reverse("add-visit-details", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == operation.views.CreateDoctorVisitView
