import datetime
import json

import pytest
from django.urls import reverse

from account.models import Rooms, Address, User
from operation.models import Bed, Operation, Admission, NurseVisit
from patients.models import TimeSlots, PatientProfile

json_data = open('operation/tests/test_data.json')
data1 = json.load(json_data)
json_data.close()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def timeslot_creation_fixture():
    timeslot31 = TimeSlots.objects.create(id=31, start_time=datetime.time(10, 00, 00), end_time=datetime.time(10, 30,
                                                                                                              00))
    timeslot32 = TimeSlots.objects.create(id=32, start_time=datetime.time(10, 00, 00), end_time=datetime.time(10, 30,
                                                                                                              00))
    timeslot1 = TimeSlots.objects.create(id=33, start_time=datetime.time(10, 00, 00),
                                         end_time=datetime.time(10, 30, 00))
    timeslot2 = TimeSlots.objects.create(id=34, start_time=datetime.time(10, 30, 00),
                                         end_time=datetime.time(11, 00, 00))
    timeslot3 = TimeSlots.objects.create(id=35, start_time=datetime.time(11, 00, 00),
                                         end_time=datetime.time(11, 30, 00))
    timeslot4 = TimeSlots.objects.create(id=36, start_time=datetime.time(11, 30, 00),
                                         end_time=datetime.time(12, 00, 00))
    timeslot5 = TimeSlots.objects.create(id=37, start_time=datetime.time(12, 00, 00),
                                         end_time=datetime.time(12, 30, 00))
    timeslot6 = TimeSlots.objects.create(id=38, start_time=datetime.time(12, 30, 00),
                                         end_time=datetime.time(13, 00, 00))
    timeslots = [timeslot1, timeslot2, timeslot3, timeslot4, timeslot5, timeslot6, timeslot31, timeslot32]
    return timeslots


@pytest.fixture
@pytest.mark.django_db
def create_receptionist():
    user = User.objects.create_user('recep1@gmail.com', 'receptionist', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Receptionist', 'Recep@123', password2='Recep@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_doctor():
    user = User.objects.create_user('doctor1@gmail.com', 'doctor', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Doctor', 'Recep@123', password2='Recep@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_admin_user():
    User.objects.create_superuser('test1@gmail.com', 'test', 'user', '7894562314', datetime.date(2016, 9, 1),
                                  'FEMALE', 'Admin@123', password2='Admin@123')
    user = User.objects.get(email='test1@gmail.com')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_shift_fixture(api_client, create_admin_user, create_surgeon, create_rooms):
    user = create_surgeon

    data = data1["create_shift_fixture_data"]
    print(data)
    url = reverse('update-shift', kwargs={'pk': user.id})
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def create_surgeon():
    user = User.objects.create_user('surgeon1@gmail.com', 'surgeon', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Surgeon', 'Surgeon@123', password2='Surgeon@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def patient_creation_fixture():
    user = User.objects.create_user('patient1@gmail.com', 'Patient', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user, disease="Appendix", advise="Operation")
    return user


@pytest.fixture
@pytest.mark.django_db
def patient_creation_fixture1():
    user = User.objects.create_user('patient1@gmail.com', 'Patient', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user)
    return user


@pytest.fixture
@pytest.mark.django_db
def create_admission_fixture(patient_creation_fixture, create_rooms, create_beds):
    patient = patient_creation_fixture
    admission = Admission.objects.create(patient=patient, bed=create_beds[0],
                                         admission_date=datetime.date(2022, 9, 15))
    return admission


@pytest.fixture
@pytest.mark.django_db
def create_rooms():
    room = Rooms.objects.create(name="A", type="Special", no_of_beds=5)
    room1 = Rooms.objects.create(name="B", type="Special", no_of_beds=5)
    room2 = Rooms.objects.create(name="X", type="GENERAL", no_of_beds=5)
    return room, room1, room2


@pytest.fixture
@pytest.mark.django_db
def create_bed(create_rooms):
    bed = Bed.objects.create(name="1", room=create_rooms[0], charges_per_day=150)
    return bed


@pytest.fixture
@pytest.mark.django_db
def create_beds(create_rooms):
    bed1 = Bed.objects.create(name="1", room=create_rooms[0], charges_per_day=150)
    bed2 = Bed.objects.create(name="2", room=create_rooms[1], charges_per_day=150, is_available=False)
    bed3 = Bed.objects.create(name="3", room=create_rooms[0], charges_per_day=150, is_available=True, is_delete=True)
    return [bed1, bed2, bed3]


@pytest.fixture
@pytest.mark.django_db
def schedule_operation_fixture(patient_creation_fixture,
                               create_surgeon, timeslot_creation_fixture):
    patient = patient_creation_fixture
    timeslot = timeslot_creation_fixture[6]
    doctor = create_surgeon
    operation = Operation.objects.create(patient=patient, doctor=doctor, timeslot=timeslot, operation_name="Hernia",
                                         date=datetime.date(2022, 9, 16), status="SCHEDULED")
    return operation


@pytest.fixture
@pytest.mark.django_db
def create_nurse():
    user = User.objects.create_user('nurse1@gmail.com', 'nurse', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Nurse', 'Nurse@123', password2='Nurse@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse_visit_fixture(create_nurse, patient_creation_fixture, schedule_operation_fixture, create_surgeon):
    nurse_visit = NurseVisit.objects.create(patient=patient_creation_fixture, nurse=create_nurse,
                                            surgeon=create_surgeon)
    return nurse_visit


class TestCreateUpdateBedView:
    @pytest.mark.django_db
    def test_add_new_bed(self, api_client, create_admin_user, create_rooms):
        room, room1, room2 = create_rooms
        data = {
            "name": 5,
            "room": room.id,
            "is_available": True,
            "charges_per_day": 150
        }
        url = reverse('add-bed')
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_update_bed1(self, api_client, create_admin_user, create_rooms, create_bed):
        bed_id = create_bed.id

        data = data1["charges_per_day_data"]
        url = reverse('update-bed', kwargs={'id': bed_id})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_bed2(self, api_client, create_admin_user, create_rooms, create_bed):
        data = data1["charges_per_day_data"]

        url = reverse('update-bed', kwargs={'id': 10})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.put(url, data=data)
        assert response.status_code == 404


class TestUpdateExistingBedAvailability:
    @pytest.mark.django_db
    def test_update_bed_availability(self, api_client, create_receptionist, create_rooms, create_bed):
        bed = create_bed
        bed_id = bed.id
        bed.is_available = False
        bed.save()

        data = data1["is_available_data"]
        url = reverse('update-bed-availability', kwargs={'id': bed_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_bed_availability1(self, api_client, create_receptionist, create_rooms, create_bed):
        bed = create_bed
        bed.is_available = False
        bed.save()
        data = data1["is_available_data"]

        url = reverse('update-bed-availability', kwargs={'id': 50})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.put(url, data=data)
        assert response.status_code == 404


class TestDeleteBedView:
    @pytest.mark.django_db
    def test_delete_bed(self, api_client, create_admin_user, create_rooms, create_bed):
        bed_id = create_bed.id
        url = reverse('delete-bed', kwargs={'id': bed_id})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.delete(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_bed1(self, api_client, create_admin_user, create_rooms, create_bed):
        bed = create_bed
        bed_id = create_bed.id
        bed.is_available = False
        bed.save()
        url = reverse('delete-bed', kwargs={'id': bed_id})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.delete(url)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_bed2(self, api_client, create_admin_user, create_rooms, create_bed):
        url = reverse('delete-bed', kwargs={'id': 50})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.delete(url)
        assert response.status_code == 404


class TestDisplayBedsView:
    @pytest.mark.django_db
    def test_show_all_beds(self, api_client, create_admin_user, create_rooms, create_bed):
        url = reverse('view-all-beds')
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_bed_details(self, api_client, create_admin_user, create_rooms, create_bed):
        bed_id = create_bed.id
        url = reverse('view-beds-detail', kwargs={'id': bed_id})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_bed_details2(self, api_client, create_admin_user, create_rooms, create_bed):
        url = reverse('view-beds-detail', kwargs={'id': 50})
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.get(url)
        assert response.status_code == 404


class TestDisplayAvailableBedsView:
    @pytest.mark.django_db
    def test_show_bed1(self, api_client, create_admin_user, create_rooms, create_beds):
        url = reverse('view-available-beds')
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_bed2(self, api_client, create_admin_user, create_rooms, create_beds):
        bed_id = create_beds[0].id
        url = reverse('view-available-beds')
        api_client.force_authenticate(user=create_admin_user)
        response = api_client.get(url, {'bed_id': bed_id})
        assert response.status_code == 200


class TestScheduleOperationView:
    @pytest.mark.django_db
    def test_schedule_operation1(self, api_client, create_admin_user, create_receptionist, patient_creation_fixture1,
                                 create_rooms, create_beds,
                                 create_surgeon, create_shift_fixture, timeslot_creation_fixture):
        timeslot = timeslot_creation_fixture[0].id
        patient = patient_creation_fixture1
        patient_id = patient.id
        doctor = create_surgeon.id
        data = {
            "doctor": doctor,
            "operation-name": "Hernia",
            "date": "2022-09-16",
            "timeslot": timeslot
        }
        url = reverse('schedule-operation', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_schedule_operation2(self, api_client, create_admin_user, create_receptionist, patient_creation_fixture,
                                 create_rooms, create_beds,
                                 create_surgeon, create_shift_fixture, timeslot_creation_fixture):
        timeslot = timeslot_creation_fixture[0].id
        patient = patient_creation_fixture
        patient.advise = "Medication"
        patient.save()
        doctor = create_surgeon.id
        data = {
            "doctor": doctor,
            "operation-name": "Hernia",
            "date": "2022-09-16",
            "timeslot": timeslot
        }
        url = reverse('schedule-operation', kwargs={'patient_id': 90})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_schedule_operation(self, api_client, create_admin_user, create_receptionist, patient_creation_fixture,
                                create_rooms, create_beds,
                                create_surgeon, create_shift_fixture, timeslot_creation_fixture):
        timeslot = timeslot_creation_fixture[6].id
        patient_id = patient_creation_fixture.id
        doctor = create_surgeon.id
        data = {
            "doctor": doctor,
            "operation_name": "Hernia",
            "date": "2022-09-19",
            "timeslot": timeslot
        }
        url = reverse('schedule-operation', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 201


class TestShowOperationsView:
    @pytest.mark.django_db
    def test_get_all_operations(self, api_client, create_admin_user, create_receptionist, patient_creation_fixture,
                                create_rooms, create_beds, create_surgeon, create_shift_fixture,
                                timeslot_creation_fixture, schedule_operation_fixture):
        url = reverse('view-all-operations')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_all_operations1(self, api_client, create_admin_user, create_receptionist, patient_creation_fixture,
                                 create_rooms, create_beds, create_surgeon, create_shift_fixture,
                                 timeslot_creation_fixture, schedule_operation_fixture):
        operation_id = schedule_operation_fixture.id
        url = reverse('view-all-operations')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url, {'op_id': operation_id})
        assert response.status_code == 200


class TestShowTodayDoctorOperationView:
    @pytest.mark.django_db
    def test_filter_operations_by_doctor_today(self, api_client, create_admin_user, create_receptionist,
                                               patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                               create_shift_fixture, timeslot_creation_fixture,
                                               schedule_operation_fixture):
        doctor = create_surgeon.id
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-doctors-operations-today', kwargs={'doctor_id': doctor})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filter_operations_by_doctor_today1(self, api_client, create_admin_user, create_receptionist,
                                                patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                                create_shift_fixture, timeslot_creation_fixture,
                                                schedule_operation_fixture):
        doctor = create_surgeon.id
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        operation_id = schedule_operation_fixture.id
        url = reverse('view-doctors-operations-today', kwargs={'doctor_id': doctor})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url, {'op_id': operation_id})
        assert response.status_code == 200


class TestShowDoctorOperationView:
    @pytest.mark.django_db
    def test_filter_operations_by_doctor(self, api_client, create_admin_user, create_receptionist,
                                         patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                         create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        doctor = create_surgeon.id
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-doctors-operations', kwargs={'doctor_id': doctor})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filter_operations_by_doctor1(self, api_client, create_admin_user, create_receptionist,
                                          patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                          create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-doctors-operations', kwargs={'doctor_id': 60})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 404


class TestShowDoctorListOperationView:
    @pytest.mark.django_db
    def test_show_my_operations(self, api_client, create_admin_user, create_receptionist,
                                patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-my-operations')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_my_operations1(self, api_client, create_admin_user, create_receptionist,
                                 patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                 create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        operation = schedule_operation_fixture
        op_id = operation.id
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-my-operations')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url, {'op_id': op_id})
        assert response.status_code == 200


class TestShowDoctorListOperationTodayView:
    @pytest.mark.django_db
    def test_show_my_operations_today(self, api_client, create_admin_user, create_receptionist,
                                      patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                      create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-my-operations-today')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_my_operations_today1(self, api_client, create_admin_user, create_receptionist,
                                       patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                       create_shift_fixture, timeslot_creation_fixture, schedule_operation_fixture):
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        op_id = operation.id
        url = reverse('view-my-operations-today')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url, {'op_id': op_id})
        assert response.status_code == 200


class TestTodayOperationView:
    @pytest.mark.django_db
    def test_get_all_operations_today_details(self, api_client, create_admin_user, create_receptionist,
                                              patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                              create_shift_fixture, timeslot_creation_fixture,
                                              schedule_operation_fixture):

        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('view-todays-operations')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_all_operations_today_details1(self, api_client, create_admin_user, create_receptionist,
                                               patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                               create_shift_fixture, timeslot_creation_fixture,
                                               schedule_operation_fixture):
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        operation_id = schedule_operation_fixture.id
        url = reverse('view-todays-operations')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url, {'op_id': operation_id})
        assert response.status_code == 200


class TestUpdateOperationView:
    @pytest.mark.django_db
    def test_update_operation_status(self, api_client, create_admin_user, create_receptionist,
                                     patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                     create_shift_fixture, timeslot_creation_fixture,
                                     schedule_operation_fixture):
        data = data1["status_completed_data"]
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        operation_id = schedule_operation_fixture.id
        url = reverse('update-operations-detail', kwargs={'op_id': operation_id})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_operation_status1(self, api_client, create_admin_user, create_receptionist,
                                      patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                      create_shift_fixture, timeslot_creation_fixture,
                                      schedule_operation_fixture):
        data = data1["status_completed_data"]
        operation = schedule_operation_fixture
        operation.date = datetime.date.today()
        operation.save()
        url = reverse('update-operations-detail', kwargs={'op_id': 60})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.put(url, data=data)
        assert response.status_code == 404


class TestCreatePatientAdmissionDetailsView:
    @pytest.mark.django_db
    def test_new_patient_admission(self, api_client, create_admin_user, create_receptionist,
                                   patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                   create_shift_fixture, timeslot_creation_fixture,
                                   schedule_operation_fixture):
        patient = patient_creation_fixture
        data = {
            "patient": patient.id,
            "bed": create_beds[0].id
        }
        url = reverse('create-admit-patient')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_new_patient_admission1(self, api_client, create_admin_user, create_receptionist,
                                    patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                    create_shift_fixture, timeslot_creation_fixture,
                                    schedule_operation_fixture):
        data = {
            "patient": 100,
            "bed": create_beds[0].id
        }
        url = reverse('create-admit-patient')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 400


class TestUpdatePatientAdmissionDetailsView:
    @pytest.mark.django_db
    def test_update_patient_admission(self, api_client, create_admin_user, create_receptionist,
                                      patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                      create_shift_fixture, timeslot_creation_fixture,
                                      schedule_operation_fixture, create_admission_fixture):
        data = data1["test_update_patient_admission_data"]
        admission_id = create_admission_fixture.id
        url = reverse('update-admit-patient-discharge-date', kwargs={'admission_id': admission_id})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.put(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_patient_admission1(self, api_client, create_admin_user, create_receptionist,
                                       patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                       create_shift_fixture, timeslot_creation_fixture,
                                       schedule_operation_fixture, create_admission_fixture):
        data = data1["test_update_patient_admission_data"]
        url = reverse('update-admit-patient-discharge-date', kwargs={'admission_id': 90})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_update_patient_admission2(self, api_client, create_admin_user, create_receptionist,
                                       patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                       create_shift_fixture, timeslot_creation_fixture,
                                       schedule_operation_fixture, create_admission_fixture):
        data = data1["test_update_patient_admission2_data"]
        admission_id = create_admission_fixture.id
        url = reverse('update-admit-patient-discharge-date', kwargs={'admission_id': admission_id})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.put(url, data=data)
        assert response.status_code == 400


class TestShowPatientAdmissionDetailsView:
    @pytest.mark.django_db
    def test_get_patient_admission_details(self, api_client, create_admin_user, create_receptionist,
                                           patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                           create_shift_fixture, timeslot_creation_fixture,
                                           schedule_operation_fixture, create_admission_fixture):
        admission_id = create_admission_fixture.id
        url = reverse('view-admissions-detail', kwargs={'admission_id': admission_id})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_patient_admission_details1(self, api_client, create_admin_user, create_receptionist,
                                            patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                            create_shift_fixture, timeslot_creation_fixture,
                                            schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-admissions-detail', kwargs={'admission_id': 50})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 404


class TestDisplayCurrentlyAdmittedPatientsView:
    @pytest.mark.django_db
    def test_get_currently_admitted_patients(self, api_client, create_admin_user, create_receptionist,
                                             patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                             create_shift_fixture, timeslot_creation_fixture,
                                             schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-active-admissions')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200


class TestDisplayAllAdmittedPatientsView:
    @pytest.mark.django_db
    def test_view_all_admissions(self, api_client, create_admin_user, create_receptionist,
                                 patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                 create_shift_fixture, timeslot_creation_fixture,
                                 schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-all-admissions')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200


class TestCreateNurseVisitView:
    @pytest.mark.django_db
    def test_add_visit_nurse(self, api_client, create_admin_user, create_receptionist, create_nurse,
                             patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                             create_shift_fixture, timeslot_creation_fixture,
                             schedule_operation_fixture, create_admission_fixture):
        data = {}
        patient_id = patient_creation_fixture.id
        url = reverse('add-nurse-visit-details', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add_visit_nurse(self, api_client, create_admin_user, create_receptionist, create_nurse,
                             patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                             create_shift_fixture, timeslot_creation_fixture,
                             schedule_operation_fixture, create_admission_fixture):
        data = {}
        url = reverse('add-nurse-visit-details', kwargs={'patient_id': 90})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_show_nurse_visit(self, api_client, create_admin_user, create_receptionist, create_nurse,
                              patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                              create_shift_fixture, timeslot_creation_fixture,
                              schedule_operation_fixture, create_admission_fixture, create_nurse_visit_fixture):
        url = reverse('show-nurse-visit-details')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200


class TestCreateDoctorVisitView:
    @pytest.mark.django_db
    def test_add_doctor_visit(self, api_client, create_admin_user, create_receptionist, create_nurse,
                              patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                              create_shift_fixture, timeslot_creation_fixture,
                              schedule_operation_fixture, create_admission_fixture):
        data = data1["is_normal_data"]
        patient_id = patient_creation_fixture.id
        url = reverse('add-visit-details', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_add_doctor_visit1(self, api_client, create_admin_user, create_receptionist, create_nurse,
                               patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                               create_shift_fixture, timeslot_creation_fixture,
                               schedule_operation_fixture, create_admission_fixture):
        data = data1["is_normal_data"]
        url = reverse('add-visit-details', kwargs={'patient_id': 90})
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_show_doctor_visit1(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                create_shift_fixture, timeslot_creation_fixture,
                                schedule_operation_fixture, create_admission_fixture):
        url = reverse('show-visit-details')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200


class TestPatientVisitView:
    @pytest.mark.django_db
    def test_get_visit_details_by_patient(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                          patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                          create_shift_fixture, timeslot_creation_fixture,
                                          schedule_operation_fixture, create_admission_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse('view-post-op-visits', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_visit_details_by_patient1(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                           patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                           create_shift_fixture, timeslot_creation_fixture,
                                           schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-post-op-visits', kwargs={'patient_id': 100})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 404


class TestDisplayScheduledPatientOperationView:
    @pytest.mark.django_db
    def test_get_scheduled_operations(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                      patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                      create_shift_fixture, timeslot_creation_fixture,
                                      schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-patients-Op-scheduled')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_scheduled_operations1(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                       patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                       create_shift_fixture, timeslot_creation_fixture,
                                       schedule_operation_fixture, create_admission_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse('view-patients-Op-scheduled-details', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_scheduled_operations2(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                       patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                       create_shift_fixture, timeslot_creation_fixture,
                                       schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-patients-Op-scheduled-details', kwargs={'patient_id': 100})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 404


class TestDisplayAllPatientOperationView:
    @pytest.mark.django_db
    def test_get_operation_details(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                   patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                   create_shift_fixture, timeslot_creation_fixture,
                                   schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-patients-Op-all')
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_operation_details1(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                    patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                    create_shift_fixture, timeslot_creation_fixture,
                                    schedule_operation_fixture, create_admission_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse('view-patients-Op-all-details', kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_operation_details2(self, api_client, create_admin_user, create_receptionist, create_nurse,
                                    patient_creation_fixture, create_rooms, create_beds, create_surgeon,
                                    create_shift_fixture, timeslot_creation_fixture,
                                    schedule_operation_fixture, create_admission_fixture):
        url = reverse('view-patients-Op-all-details', kwargs={'patient_id': 100})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 404
