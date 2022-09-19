import pytest
from django.urls import reverse, resolve

import patients


@pytest.mark.django_db
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_display_registered_patients_url(api_client):
    url = reverse("display-registered-patients")
    assert resolve(url).func.view_class == patients.views.ShowRegisteredPatientView


@pytest.mark.django_db
def test_display_patient_details_url(api_client):
    url = reverse("display-patient-details", kwargs={'pk': 1})
    assert resolve(url).func.view_class == patients.views.ShowRegisteredPatientView


@pytest.mark.django_db
def test_patient_registration_url(api_client):
    url = reverse("patient-registration")
    assert resolve(url).func.view_class == patients.views.PatientRegistrationView


@pytest.mark.django_db
def test_update_patient_url(api_client):
    url = reverse("update-patient", kwargs={'pk': 1})
    assert resolve(url).func.view_class == patients.views.PatientRegistrationView


@pytest.mark.django_db
def test_time_slots_url(api_client):
    url = reverse("time-slots")
    assert resolve(url).func.view_class == patients.views.ViewAvailableTimeSlots


@pytest.mark.django_db
def test_available_doctors_url(api_client):
    url = reverse("available-doctors")
    assert resolve(url).func.view_class == patients.views.ViewAllDoctors


@pytest.mark.django_db
def test_book_appointment_url(api_client):
    url = reverse("book-appointment", kwargs={'pk': 1})
    assert resolve(url).func.view_class == patients.views.BookAppointmentView


@pytest.mark.django_db
def test_cancel_appointment_url(api_client):
    url = reverse("cancel-appointment", kwargs={'pk': 1, 'pk1': 1})
    assert resolve(url).func.view_class == patients.views.UpdateAppointmentView


@pytest.mark.django_db
def test_appointments_for_doctor_url(api_client):
    url = reverse("appointments-for-doctor")
    assert resolve(url).func.view_class == patients.views.ShowDoctorsAppointmentsView


@pytest.mark.django_db
def test_appointments_url(api_client):
    url = reverse("appointments")
    assert resolve(url).func.view_class == patients.views.ShowAllAppointmentView


@pytest.mark.django_db
def test_appointments_url(api_client):
    url = reverse("today-appointments")
    assert resolve(url).func.view_class == patients.views.ShowTodaysAppointmentView


@pytest.mark.django_db
def test_filter_by_url(api_client):
    url = reverse("filter-by")
    assert resolve(url).func.view_class == patients.views.FilterDoctorAppointmentView


@pytest.mark.django_db
def test_medication_url(api_client):
    url = reverse("medication")
    assert resolve(url).func.view_class == patients.views.CreateMedicationView


@pytest.mark.django_db
def test_show_patients_prescription_url(api_client):
    url = reverse("show-patients-prescription", kwargs={'patient_id': 1})
    assert resolve(url).func.view_class == patients.views.ShowMedicationView


@pytest.mark.django_db
def test_add_medicines_to_prescription_url(api_client):
    url = reverse("add-medicines-to-prescription", kwargs={'id': 1})
    assert resolve(url).func.view_class == patients.views.UpdateMedicationView


@pytest.mark.django_db
def test_update_medicines_in_prescription_url(api_client):
    url = reverse("update-medicine-in-prescription", kwargs={'id1': 1, 'id2': 2})
    assert resolve(url).func.view_class == patients.views.UpdateMedicationView


@pytest.mark.django_db
def test_remove_medicines_from_prescription_url(api_client):
    url = reverse("remove-medicine-from-prescription", kwargs={'id1': 1, 'id2': 2})
    assert resolve(url).func.view_class == patients.views.UpdateMedicationView


@pytest.mark.django_db
def test_update_health_details_url(api_client):
    url = reverse("update-health-details", kwargs={'id': 1})
    assert resolve(url).func.view_class == patients.views.UpdatePatientHealthDetails
