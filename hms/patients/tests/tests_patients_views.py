import datetime
import json
from datetime import date

import pytest
from django.urls import reverse

from account.models import User, Address, Rooms
from patients.models import TimeSlots, Appointment, PatientProfile, Prescription, Medication

json_data = open('patients/tests/test_data.json')
data1 = json.load(json_data)
json_data.close()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def timeslot_creation_fixture():
    timeslot1 = TimeSlots.objects.create(start_time=datetime.time(10, 00, 00), end_time=datetime.time(10, 30, 00))
    timeslot2 = TimeSlots.objects.create(start_time=datetime.time(10, 30, 00), end_time=datetime.time(11, 00, 00))
    timeslot3 = TimeSlots.objects.create(start_time=datetime.time(11, 00, 00), end_time=datetime.time(11, 30, 00))
    timeslot4 = TimeSlots.objects.create(start_time=datetime.time(11, 30, 00), end_time=datetime.time(12, 00, 00))
    timeslot5 = TimeSlots.objects.create(start_time=datetime.time(12, 00, 00), end_time=datetime.time(12, 30, 00))
    timeslot6 = TimeSlots.objects.create(start_time=datetime.time(12, 30, 00), end_time=datetime.time(13, 00, 00))
    timeslots = [timeslot1, timeslot2, timeslot3, timeslot4, timeslot5, timeslot6]
    return timeslots


@pytest.fixture
@pytest.mark.django_db
def create_receptionist():
    user = User.objects.create_user('recep1@gmail.com', 'receptionist', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Receptionist', 'Recep@123', password2='Recep@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_doctor():
    user = User.objects.create_user('doctor1@gmail.com', 'doctor', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Doctor', 'Recep@123', password2='Recep@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_admin_user():
    User.objects.create_superuser('test1@gmail.com', 'test', 'user', '7894562314', date(2016, 9, 1),
                                  'FEMALE', 'Admin@123', password2='Admin@123')
    user = User.objects.get(email='test1@gmail.com')
    return user


@pytest.fixture
@pytest.mark.django_db
def patient_creation_fixture():
    user = User.objects.create_user('patient1@gmail.com', 'Patient', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user)
    return user


@pytest.fixture
@pytest.mark.django_db
def create_rooms():
    room = Rooms.objects.create(name="A", type="Special", no_of_beds=5)
    room1 = Rooms.objects.create(name="B", type="Special", no_of_beds=5)
    room2 = Rooms.objects.create(name="X", type="GENERAL", no_of_beds=5)
    return room, room1, room2


@pytest.fixture
@pytest.mark.django_db
def create_shift_fixture(api_client, create_admin_user, create_doctor, create_rooms):
    user = create_doctor
    data = data1["create_shift_fixture_data"]
    url = reverse('update-shift', kwargs={'pk': user.id})
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def create_prescription_fixture(patient_creation_fixture):
    patient = patient_creation_fixture
    prescription = Prescription.objects.create(date=date(2022, 9, 14), patient=patient, for_no_days=5)
    Medication.objects.create(name="Dan-P", brand="UNISON", dose_per_day=2,
                              how_to_consume="Morning-Evening",
                              prescription=prescription)
    Medication.objects.create(name="Mox", brand="UNISON", dose_per_day=2,
                              how_to_consume="Morning-Evening",
                              prescription=prescription)
    return prescription


class TestPatientRegistrationView:
    @pytest.mark.django_db
    def test_register_patient(self, api_client, create_receptionist):
        data = data1["register-patient-1"]
        url = reverse('patient-registration')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_register_patient2(self, api_client, create_receptionist):
        data = data1["register-patient-2"]
        url = reverse('patient-registration')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_patient1(self, api_client, create_receptionist, patient_creation_fixture):
        patient = patient_creation_fixture
        patient_id = patient.id
        data = data1["update-patient-data-1"]
        url = reverse('update-patient', kwargs={'pk': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == 200


@pytest.fixture
@pytest.mark.django_db
def test_update_patient2(self, api_client, create_receptionist, patient_creation_fixture):
    data = data1["update-patient-data-1"]
    url = reverse('update-patient', kwargs={'pk': 15})
    api_client.force_authenticate(user=create_receptionist)
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 404


class TestShowRegisteredPatients:
    @pytest.mark.django_db
    def test_display_patient(self, api_client, create_receptionist, patient_creation_fixture):
        url = reverse('display-registered-patients')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_display_patient1(self, api_client, create_receptionist, patient_creation_fixture):
        patient = patient_creation_fixture
        patient_id = patient.id
        url = reverse('display-patient-details', kwargs={'pk': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestViewAllDoctorsView:
    @pytest.mark.django_db
    def test_display_all_doctors(self, api_client, create_receptionist, create_doctor):
        url = reverse('available-doctors')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestBookAppointmentView:
    @pytest.mark.django_db
    def test_book_appointment(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                              patient_creation_fixture, timeslot_creation_fixture):
        doctor = create_doctor.id
        patient = patient_creation_fixture.id
        data = {
            "date": "2022-09-16",
            "timeslot": timeslot_creation_fixture[0].id,
            "doctor": doctor
        }
        url = reverse('book-appointment', kwargs={'pk': patient})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_book_appointment1(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                               patient_creation_fixture, timeslot_creation_fixture):
        doctor = create_doctor.id
        data = {
            "date": "2022-09-14",
            "timeslot": "1",
            "doctor": doctor
        }
        url = reverse('book-appointment', kwargs={'pk': 50})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_book_appointment2(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                               patient_creation_fixture, timeslot_creation_fixture):
        doctor = create_doctor.id
        patient = patient_creation_fixture.id
        data = {
            "date": "2022-09-05",
            "timeslot": "1",
            "doctor": doctor
        }
        url = reverse('book-appointment', kwargs={'pk': patient})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 400


#
class TestUpdateAppointmentView:
    @pytest.mark.django_db
    def test_cancel_appointment(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                patient_creation_fixture, timeslot_creation_fixture):
        patient = patient_creation_fixture.id
        appointment = Appointment.objects.create(date=date(year=2022, month=9, day=15),
                                                 patient=patient_creation_fixture, doctor=create_doctor,
                                                 timeslot=timeslot_creation_fixture[0], status="SCHEDULED")

        data = data1["status_cancelled_data"]
        url = reverse('cancel-appointment', kwargs={'pk': patient, 'pk1': appointment.id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_cancel_appointment1(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                 patient_creation_fixture, timeslot_creation_fixture):
        appointment = Appointment.objects.create(date=date(year=2022, month=9, day=15),
                                                 patient=patient_creation_fixture, doctor=create_doctor,
                                                 timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        data = data1["status_cancelled_data"]

        url = reverse('cancel-appointment', kwargs={'pk': 80, 'pk1': appointment.id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_cancel_appointment2(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                 patient_creation_fixture, timeslot_creation_fixture):
        patient = patient_creation_fixture.id
        Appointment.objects.create(date=date(year=2022, month=9, day=15),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        data = data1["status_cancelled_data"]
        url = reverse('cancel-appointment', kwargs={'pk': patient, 'pk1': 60})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data)
        assert response.status_code == 404


class TestShowAllAppointmentView:
    @pytest.mark.django_db
    def test_show_all_appointments(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                   patient_creation_fixture, timeslot_creation_fixture):
        Appointment.objects.create(date=date(year=2022, month=9, day=15),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('appointments')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestShowTodayAppointmentView:
    @pytest.mark.django_db
    def test_show_today_appointments(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                     patient_creation_fixture, timeslot_creation_fixture):
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('today-appointments')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestFilterDoctorAppointmentView:
    @pytest.mark.django_db
    def test_filter_by_doctor_appointments(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                           patient_creation_fixture, timeslot_creation_fixture):
        doctor = create_doctor.first_name
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('filter-by')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url, {'first_name': doctor})
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filter_by_doctor_appointments2(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                            patient_creation_fixture, timeslot_creation_fixture):
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('filter-by')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url, {'first_name': 15})
        assert response.status_code == 404


class TestUpdatePatientHealthDetailsView:
    @pytest.mark.django_db
    def test_update_patient_health_details1(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                            patient_creation_fixture, timeslot_creation_fixture):
        patient_id = patient_creation_fixture.id
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")

        data = data1["test_update_patient_health_details1_data"]
        url = reverse('update-health-details', kwargs={'id': patient_id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_patient_health_details2(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                            patient_creation_fixture, timeslot_creation_fixture):
        patient_id = patient_creation_fixture.id
        data = data1["test_update_patient_health_details1_data"]
        url = reverse('update-health-details', kwargs={'id': patient_id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_patient_health_details3(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                            patient_creation_fixture, timeslot_creation_fixture):
        data = data1["test_update_patient_health_details1_data"]
        url = reverse('update-health-details', kwargs={'id': 50})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.put(url, data=data)
        assert response.status_code == 404


class TestCreateMedicationView:
    @pytest.mark.django_db
    def test_create_medication_view(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                    patient_creation_fixture, timeslot_creation_fixture):
        patient = patient_creation_fixture
        appointment = Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                                 patient=patient_creation_fixture, doctor=create_doctor,
                                                 timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        data = {
            "patient": patient.id,
            "medication": [
                {"name": "Azithromycin", "brand": "Unison", "dose_per_day": 2,
                 "how_to_consume": "Morning-Night after meal"}
            ],
            "for_no_days": 10
        }
        url = reverse('medication')
        api_client.force_authenticate(user=create_doctor)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 201


class TestUpdateMedicationView:
    @pytest.mark.django_db
    def test_add_medicine_to_prescription(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                          patient_creation_fixture, timeslot_creation_fixture,
                                          create_prescription_fixture):
        prescription_id = create_prescription_fixture.id
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")

        data = data1["test_add_medicine_to_prescription_data"]

        url = reverse('add-medicines-to-prescription', kwargs={'id': prescription_id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_add_medicine_to_prescription1(self, api_client, create_receptionist, create_doctor,
                                           create_shift_fixture,
                                           patient_creation_fixture, timeslot_creation_fixture,
                                           ):
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        data = data1["test_add_medicine_to_prescription_data"]

        url = reverse('add-medicines-to-prescription', kwargs={'id': 80})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.post(url, data=data, format="json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_update_medicine_in_prescription(self, api_client, create_receptionist, create_doctor, create_shift_fixture,
                                             patient_creation_fixture, timeslot_creation_fixture,
                                             create_prescription_fixture):
        prescription_id = create_prescription_fixture.id
        medications = Medication.objects.filter(prescription=prescription_id)
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")

        data = data1["test_update_medicine_in_prescription_data"]
        url = reverse('update-medicine-in-prescription', kwargs={'id1': prescription_id, 'id2': medications[0].id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_medicine_in_prescription1(self, api_client, create_receptionist, create_doctor,
                                              create_shift_fixture,
                                              patient_creation_fixture, timeslot_creation_fixture,
                                              create_prescription_fixture):
        prescription_id = create_prescription_fixture.id
        medications = Medication.objects.filter(prescription=prescription_id)
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        data = data1["test_update_medicine_in_prescription_data"]

        url = reverse('update-medicine-in-prescription', kwargs={'id1': 50, 'id2': medications[0].id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_remove_medicine_from_prescription(self, api_client, create_receptionist, create_doctor,
                                               create_shift_fixture,
                                               patient_creation_fixture, timeslot_creation_fixture,
                                               create_prescription_fixture):
        prescription_id = create_prescription_fixture.id
        medications = Medication.objects.filter(prescription=prescription_id)
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('update-medicine-in-prescription', kwargs={'id1': prescription_id, 'id2': medications[0].id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.delete(url)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_remove_medicine_from_prescription1(self, api_client, create_receptionist, create_doctor,
                                                create_shift_fixture,
                                                patient_creation_fixture, timeslot_creation_fixture,
                                                create_prescription_fixture):
        prescription_id = create_prescription_fixture.id
        medications = Medication.objects.filter(prescription=prescription_id)
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('update-medicine-in-prescription', kwargs={'id1': 50, 'id2': medications[0].id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.delete(url)
        assert response.status_code == 404


class TestShowMedicationView:
    @pytest.mark.django_db
    def test_show_prescription(self, api_client, create_receptionist, create_doctor,
                               create_shift_fixture,
                               patient_creation_fixture, timeslot_creation_fixture,
                               create_prescription_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse('show-patients-prescription', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_prescription1(self, api_client, create_receptionist, create_doctor,
                                create_shift_fixture,
                                patient_creation_fixture, timeslot_creation_fixture,
                                create_prescription_fixture):
        url = reverse('show-patients-prescription', kwargs={'patient_id': 50})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_show_prescription2(self, api_client, create_receptionist, create_doctor,
                                create_shift_fixture,
                                patient_creation_fixture, timeslot_creation_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse('show-patients-prescription', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_doctor)
        response = api_client.get(url)
        assert response.status_code == 400


class TestShowDoctorsAppointmentsView:
    @pytest.mark.django_db
    def test_my_appointments_view(self, api_client, create_receptionist, create_doctor,
                                  create_shift_fixture,
                                  patient_creation_fixture, timeslot_creation_fixture):
        Appointment.objects.create(date=date(year=2022, month=9, day=14),
                                   patient=patient_creation_fixture, doctor=create_doctor,
                                   timeslot=timeslot_creation_fixture[0], status="SCHEDULED")
        url = reverse('appointments-for-doctor')
        api_client.force_authenticate(user=create_doctor)
        response = api_client.get(url)
        assert response.status_code == 200
