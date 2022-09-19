import datetime

import pytest
from django.urls import reverse
from account.models import User, Address, Rooms
from patients.models import TimeSlots, Appointment, PatientProfile
from operation.models import Operation, Admission, Bed
from billing.models import Bill


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def create_admin_user():
    User.objects.create_superuser('test1@gmail.com', 'test', 'user', '7894562314', datetime.date(2016, 9, 1),
                                  'FEMALE', 'Admin@123', password2='Admin@123')
    user = User.objects.get(email='test1@gmail.com')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_doctor():
    user = User.objects.create_user('doctor1@gmail.com', 'doctor', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Doctor', 'Doctor@123', password2='Doctor@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse():
    user = User.objects.create_user('nurse1@gmail.com', 'nurse', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Nurse', 'Nurse@123', password2='Nurse@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_surgeon():
    user = User.objects.create_user('surgeon1@gmail.com', 'surgeon', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Surgeon', 'Surgeon@123', password2='Surgeon@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_receptionist():
    user = User.objects.create_user('recep1@gmail.com', 'receptionist', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Receptionist', 'Recep@123', password2='Recep@123')
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
def patient_creation_fixture():
    user = User.objects.create_user('patient1@gmail.com', 'Patient', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user)
    return user


@pytest.fixture
@pytest.mark.django_db
def patient_creation_fixture1():
    user = User.objects.create_user('patient2@gmail.com', 'Patient2', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user)
    return user


@pytest.fixture
@pytest.mark.django_db
def patient_creation_fixture2():
    user = User.objects.create_user('patient3@gmail.com', 'Patient3', 'test', '7894562314', datetime.date(2016, 9, 1),
                                    'FEMALE', 'Patient', 'Patient@123', password2='Patient@123')
    Address.objects.create(user=user, block_no="5", building_name="Shreyas Apartment", city="Ahmedabad",
                           state="Gujarat", country="India", pincode="362001")
    PatientProfile.objects.create(patient_id=user)
    return user


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
def create_appointment_fixture(patient_creation_fixture, patient_creation_fixture1,
                               patient_creation_fixture2, create_doctor,
                               timeslot_creation_fixture):
    patient1 = patient_creation_fixture
    patient2 = patient_creation_fixture1
    patient3 = patient_creation_fixture2
    appointment1 = Appointment.objects.create(patient=patient1, doctor=create_doctor,
                                              date=datetime.date(2022, 9, 16), timeslot=timeslot_creation_fixture[0],
                                              status="SCHEDULED")
    appointment2 = Appointment.objects.create(patient=patient2, doctor=create_doctor,
                                              date=datetime.date(2022, 9, 16), timeslot=timeslot_creation_fixture[1],
                                              status="COMPLETED")
    appointment3 = Appointment.objects.create(patient=patient3, doctor=create_doctor,
                                              date=datetime.date(2022, 9, 16), timeslot=timeslot_creation_fixture[1],
                                              status="CANCELLED")
    return [appointment1, appointment2, appointment3]


@pytest.fixture
@pytest.mark.django_db
def create_rooms():
    room = Rooms.objects.create(name="A", type="Special", no_of_beds=5)
    room1 = Rooms.objects.create(name="B", type="Special", no_of_beds=5)
    room2 = Rooms.objects.create(name="X", type="GENERAL", no_of_beds=5)
    return room, room1, room2


@pytest.fixture
@pytest.mark.django_db
def create_beds(create_rooms):
    bed1 = Bed.objects.create(name="1", room=create_rooms[0], charges_per_day=150)
    bed2 = Bed.objects.create(name="2", room=create_rooms[1], charges_per_day=150, is_available=False)
    bed3 = Bed.objects.create(name="3", room=create_rooms[0], charges_per_day=150, is_available=True, is_delete=True)
    return [bed1, bed2, bed3]


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
def create_operation_fixture(patient_creation_fixture, patient_creation_fixture1,
                             patient_creation_fixture2, create_surgeon,
                             timeslot_creation_fixture, create_rooms, create_beds):
    operation1 = Operation.objects.create(doctor=create_surgeon, patient=patient_creation_fixture,
                                          operation_name="Appendix", date=datetime.date(2022, 9, 12),
                                          timeslot=timeslot_creation_fixture[6], status="COMPLETED")
    admission1 = Admission.objects.create(patient=patient_creation_fixture, bed=create_beds[0],
                                          admission_date=datetime.date(2022, 9, 10),
                                          discharge_date=datetime.date(2022, 9, 16))
    operation2 = Operation.objects.create(doctor=create_surgeon, patient=patient_creation_fixture1,
                                          operation_name="Appendix", date=datetime.date(2022, 9, 16),
                                          timeslot=timeslot_creation_fixture[6], status="COMPLETED")
    admission2 = Admission.objects.create(patient=patient_creation_fixture1, bed=create_beds[0],
                                          admission_date=datetime.date(2022, 9, 10),
                                          discharge_date=datetime.date(2022, 9, 18))
    operation3 = Operation.objects.create(doctor=create_surgeon, patient=patient_creation_fixture2,
                                          operation_name="Appendix", date=datetime.date(2022, 9, 16),
                                          timeslot=timeslot_creation_fixture[7], status="SCHEDULED")
    admission3 = Admission.objects.create(patient=patient_creation_fixture2, bed=create_beds[0],
                                          admission_date=datetime.date(2022, 9, 15))
    operation_list = [operation1, operation2, operation3]
    admission_list = [admission1, admission2, admission3]
    return operation_list, admission_list


@pytest.fixture
@pytest.mark.django_db
def create_bill_fixture(create_operation_fixture, create_appointment_fixture, patient_creation_fixture,
                        patient_creation_fixture1):
    patient1 = patient_creation_fixture
    patient2 = patient_creation_fixture1
    operation_list, admission_list = create_operation_fixture
    appointments = create_appointment_fixture[0].id
    print(appointments)
    bill_details1 = {'op_id': operation_list[0].id}
    bill_details2 = {'opd_id': appointments}
    bill1 = Bill.objects.create(patient=patient1, bed_charge=500, surgery_charge=500, admission_charge=700,
                                opd_charge=0,
                                total_charge=1700,
                                bill_details=bill_details1, date=datetime.date(2022, 9, 12))
    bill2 = Bill.objects.create(patient=patient2, bed_charge=0, surgery_charge=0, admission_charge=0, opd_charge=600,
                                total_charge=600,
                                bill_details=bill_details2, date=datetime.date(2022, 9, 16))
    return [bill1, bill2]


class TestGenerateOpdBillView:
    @pytest.mark.django_db
    def test_new_bill_create_opd1(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                                  create_appointment_fixture):
        appointment1 = create_appointment_fixture[0]
        patient_id = patient_creation_fixture.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-OPD")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_new_bill_create_opd2(self, api_client, create_receptionist, patient_creation_fixture1, create_doctor,
                                  create_appointment_fixture):
        appointment1 = create_appointment_fixture[1]
        patient_id = patient_creation_fixture1.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-OPD")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_new_bill_create_opd3(self, api_client, create_receptionist, patient_creation_fixture2, create_doctor,
                                  create_appointment_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture2.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-OPD")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_new_bill_create_opd4(self, api_client, create_receptionist, patient_creation_fixture2, create_doctor,
                                  create_appointment_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture2.id
        data = {
            "patient": 50
        }
        url = reverse("generate-bill-for-OPD")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404


class TestGenerateOperationBillView:
    @pytest.mark.django_db
    def test_new_bill_create_operation(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                                       create_appointment_fixture, create_operation_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-operation")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_new_bill_create_operation1(self, api_client, create_receptionist, patient_creation_fixture1, create_doctor,
                                        create_appointment_fixture, create_operation_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture1.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-operation")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_new_bill_create_operation2(self, api_client, create_receptionist, patient_creation_fixture2, create_doctor,
                                        create_appointment_fixture, create_operation_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture2.id
        data = {
            "patient": patient_id
        }
        url = reverse("generate-bill-for-operation")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_new_bill_create_operation3(self, api_client, create_receptionist, patient_creation_fixture2, create_doctor,
                                        create_appointment_fixture, create_operation_fixture):
        appointment1 = create_appointment_fixture[2]
        patient_id = patient_creation_fixture2.id
        data = {
            "patient": 50
        }
        url = reverse("generate-bill-for-operation")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.post(url, data=data)
        assert response.status_code == 404


class TestPrintPatientBillView:
    @pytest.mark.django_db
    def test_print_patient_bill(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                                create_appointment_fixture, create_operation_fixture, create_bill_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse("get-all-bills-by-patient", kwargs={'patient_id': patient_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestTodayBillsView:
    @pytest.mark.django_db
    def test_print_today_bills(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                               create_appointment_fixture, create_operation_fixture, create_bill_fixture):
        patient_id = patient_creation_fixture.id
        url = reverse("get-all-todays-bills")
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200


class TestBillDetailView:
    @pytest.mark.django_db
    def test_print_bill_detail(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                               create_appointment_fixture, create_operation_fixture, create_bill_fixture):
        patient_id = patient_creation_fixture.id
        bill_id = create_bill_fixture[0].id
        url = reverse("print-bill", kwargs={'patient_id': patient_id, 'bill_id': bill_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_print_bill_detail1(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                                create_appointment_fixture, create_operation_fixture, create_bill_fixture):
        patient_id = patient_creation_fixture.id
        bill_id = create_bill_fixture[0].id
        url = reverse("print-today-bill-details", kwargs={'bill_id': bill_id})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_print_bill_detail2(self, api_client, create_receptionist, patient_creation_fixture, create_doctor,
                                create_appointment_fixture, create_operation_fixture, create_bill_fixture):
        patient_id = patient_creation_fixture.id
        bill_id = create_bill_fixture[0].id
        url = reverse("print-today-bill-details", kwargs={'bill_id': 50})
        api_client.force_authenticate(user=create_receptionist)
        response = api_client.get(url)
        assert response.status_code == 404
