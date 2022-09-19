# Create admin
import json
from datetime import date

import pytest
from django.urls import reverse

from account.models import User, Rooms, LeaveRequest

json_data = open('account/tests/test_data.json')
data1 = json.load(json_data)
json_data.close()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def create_admin_user():
    User.objects.create_superuser('test1@gmail.com', 'test', 'user', '7894562314', date(2016, 9, 1),
                                  'FEMALE', 'Admin@123', password2='Admin@123')
    user = User.objects.get(email='test1@gmail.com')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_admin_user1():
    user = User.objects.create_superuser('test1@gmail.com', 'test', 'user', '7894562314', date(2016, 9, 1),
                                         'FEMALE', 'Admin@123', password2='Admin@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_doctor():
    user = User.objects.create_user('doctor1@gmail.com', 'doctor', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Doctor', 'Doctor@123', password2='Doctor@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse():
    user = User.objects.create_user('nurse1@gmail.com', 'nurse', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Nurse', 'Nurse@123', password2='Nurse@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse2():
    user = User.objects.create_user('nurse2@gmail.com', 'nurse2', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Nurse', 'Nurse@123', password2='Nurse@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_surgeon():
    user = User.objects.create_user('surgeon1@gmail.com', 'surgeon', 'test', '7894562314', date(2016, 9, 1),
                                    'FEMALE', 'Surgeon', 'Surgeon@123', password2='Surgeon@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_receptionist():
    user = User.objects.create_user('recep1@gmail.com', 'receptionist', 'test', '7894562314', date(2016, 9, 1),
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
def create_shift_fixture(api_client, create_admin_user1, create_surgeon, create_rooms):
    user = create_surgeon
    data = data1["create_shift_fixture_data"]
    url = reverse('update-shift', kwargs={'pk': user.id})
    api_client.force_authenticate(user=create_admin_user1)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def create_nurse_shift_fixture(api_client, create_admin_user1, create_nurse, create_rooms):
    user = create_nurse
    data = data1["create_nurse_shift_fixture_data"]
    url = reverse('update-shift', kwargs={'pk': user.id})
    api_client.force_authenticate(user=create_admin_user1)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def leave_create_fixture(api_client, create_nurse, create_rooms, create_shift_fixture):
    data = data1["leave_create_fixture_data"]
    url = reverse('my-leaves')
    api_client.force_authenticate(user=create_nurse)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def approve_leave_fixture(api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                          leave_create_fixture):
    employee_id = create_nurse.id
    leave = LeaveRequest.objects.filter(employee=employee_id)
    leave_id = leave[0].id
    data = data1["approve_leave_fixture_data"]
    url = reverse('all-leaves', kwargs={'pk': leave_id})
    api_client.force_authenticate(user=create_admin_user1)
    response = api_client.put(url, data=data)
    return response


@pytest.fixture()
@pytest.mark.django_db
def assign_substitute_fixture(api_client, create_admin_user1, create_nurse, create_nurse2, create_rooms,
                              create_nurse_shift_fixture,
                              leave_create_fixture, approve_leave_fixture):
    substitute = create_nurse2.email
    employee_id = create_nurse.id
    leave = LeaveRequest.objects.filter(employee=employee_id)
    leave_id = leave[0].id
    data = {
        "for_date": "2022-12-28",
        "substitute": substitute
    }
    url = reverse('assign-substitute', kwargs={'pk': leave_id})
    api_client.force_authenticate(user=create_admin_user1)
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def login_admin(api_client):
    """
    Valid credentials
    """

    data = data1["login_admin_data"]
    url = reverse("admin-login")
    response = api_client.post(url, data=data)
    return response


@pytest.fixture
@pytest.mark.django_db
def login_admin1(api_client):
    """
    Valid credentials
    """
    data = data1["login_admin1_data"]
    url = reverse("admin-login")
    response = api_client.post(url, data=data)
    return response


class TestUsers:

    @pytest.mark.django_db
    def test_login_user_valid(self, api_client, create_admin_user):
        """
        Valid credentials
        """
        data = data1["test_login_user_valid_data"]
        url = reverse("admin-login")
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_login_user_invalid_1(self, api_client, create_admin_user):
        """
        Invalid credentials
        """
        data = data1["test_login_user_invalid_1_data"]
        url = reverse("admin-login")
        response = api_client.post(url, data=data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_login_user_invalid_2(self, api_client, create_admin_user):
        """
        Incomplete fields
        """
        data = data1["test_login_user_invalid_2_data"]
        url = reverse("admin-login")
        response = api_client.post(url, data=data)
        assert response.status_code == 400


class TestUsersListView:
    @pytest.mark.django_db
    def test_users_list_1(self, api_client, create_admin_user1):
        url = reverse("view-all-users")
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        print(response)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_users_list_2(self, api_client, create_nurse):
        url = reverse("view-all-users")
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 403


class TestRegisterUsersView:

    @pytest.mark.django_db
    def test_create_user_1(self, api_client, create_admin_user1):
        data = data1["test_create_user_1_data"]
        url = reverse('register')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create_user_2(self, api_client, create_nurse):
        data = data1["test_create_user_2_data"]

        url = reverse('register')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 403


class TestShiftCreateView:

    @pytest.mark.django_db
    def test_create_shift(self, api_client, create_admin_user1, create_nurse, create_rooms):
        user = create_nurse
        data = data1["test_create_shift_data"]
        url = reverse('update-shift', kwargs={'pk': user.id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create_shift_1(self, api_client, create_admin_user1, create_nurse, create_rooms):
        user = create_nurse
        data = data1["test_create_shift_1_data"]

        url = reverse('update-shift', kwargs={'pk': user.id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_shift_2(self, api_client, create_admin_user1, create_surgeon, create_rooms):
        user = create_surgeon

        data = data1["test_create_shift_2_data"]
        url = reverse('update-shift', kwargs={'pk': user.id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_show_shift_1(self, api_client, create_admin_user1, create_surgeon, create_rooms, create_shift_fixture):
        user = create_surgeon
        url = reverse('update-shift', kwargs={'pk': user.id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_shift_2(self, api_client, create_admin_user1, create_surgeon, create_rooms, create_shift_fixture):
        url = reverse('update-shift')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200


class TestEmployeeShiftView:
    @pytest.mark.django_db
    def test_show_my_shifts_1(self, api_client, create_surgeon, create_rooms, create_shift_fixture):
        url = reverse('view-shift')
        api_client.force_authenticate(user=create_surgeon)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_show_my_shifts_2(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        url = reverse('view-shift')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 400


class TestEmployeeProfileView:
    @pytest.mark.django_db
    def test_show_my_profile(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        url = reverse('view-profile')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_my_profile(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        data = data1["test_update_my_profile_data"]
        url = reverse('view-profile')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url, data=data)
        assert response.status_code == 200


class TestMonthlyScheduleView:
    @pytest.mark.django_db
    def test_monthly_schedule(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        url = reverse('view-schedule')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200


class TestLeaveCreateView:
    @pytest.mark.django_db
    def test_leave_create_view(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        data = data1["test_leave_create_view_data"]
        url = reverse('my-leaves')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_leave_create_view1(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        data = data1["test_leave_create_view1_data"]
        url = reverse('my-leaves')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_leave_create_view2(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        data = data1["test_leave_create_view2_data"]
        url = reverse('my-leaves')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_leave_display_view(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                leave_create_fixture):
        url = reverse('my-leaves')
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_leave_display_view2(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        url = reverse('my-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_leave_display_view3(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        url = reverse('my-leaves', kwargs={'pk': 80})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_leave_update_view(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                               leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(leave[0].id)
        leave_id = leave[0].id

        data = data1["test_leave_update_view_data"]
        url = reverse('my-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_leave_update_view3(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                leave_create_fixture, approve_leave_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(leave[0].id)
        leave_id = leave[0].id
        data = data1["test_leave_update_view_data"]
        url = reverse('my-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_leave_update_view4(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                leave_create_fixture, approve_leave_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(leave[0].id)
        leave_id = leave[0].id
        data = data1["test_leave_update_view_data"]

        url = reverse('my-leaves', kwargs={'pk': 60})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_leave_update_view2(self, api_client, create_nurse, create_nurse2, create_rooms, create_shift_fixture,
                                leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(leave[0].id)
        leave_id = leave[0].id
        data = data1["test_leave_update_view_data"]

        url = reverse('my-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse2)
        response = api_client.put(url, data=data)
        assert response.status_code == 400


class TestDeleteLeaveView:

    @pytest.mark.django_db
    def test_leave_delete_view(self, api_client, create_nurse, create_nurse2, create_rooms, create_shift_fixture,
                               leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        url = reverse('delete-leave', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse2)
        response = api_client.put(url)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_leave_delete_view1(self, api_client, create_nurse, create_rooms, create_shift_fixture,
                                leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        url = reverse('delete-leave', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_leave_delete_view2(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.create(employee=create_nurse, from_date=date(year=2022, month=9, day=6),
                                            to_date=date(year=2022, month=9, day=7), reason="For planned trip",
                                            status="ACCEPTED")
        leave_id = leave.id
        url = reverse('delete-leave', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_leave_delete_view3(self, api_client, create_nurse, create_rooms, create_shift_fixture):
        url = reverse('delete-leave', kwargs={'pk': 5})
        api_client.force_authenticate(user=create_nurse)
        response = api_client.put(url)
        assert response.status_code == 404


class TestLeaveApprovalDisapprovalView:
    @pytest.mark.django_db
    def test_display_all_view(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                              leave_create_fixture):
        url = reverse('all-leaves')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_display_all_view1(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                               leave_create_fixture):
        url = reverse('all-leaves', kwargs={'pk': 5})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_display_all_view2(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                               leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_approve_leave_view(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        data = data1["status_accepted_data"]
        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_approve_leave_view1(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        data = data1["status_accepted_data"]
        url = reverse('all-leaves', kwargs={'pk': 80})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_approve_leave_view2(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.get(employee=employee_id)
        leave.status = "ACCEPTED"
        leave_id = leave.id
        leave.save()
        data = data1["status_accepted_data"]

        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_approve_leave_view3(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.get(employee=employee_id)
        leave.status = "REJECTED"
        leave_id = leave.id
        leave.save()
        data = data1["status_accepted_data"]

        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_approve_leave_view4(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.get(employee=employee_id)
        leave.status = "ACCEPTED"
        leave_id = leave.id
        leave.save()
        data = data1["status_rejected_data"]
        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_approve_leave_view5(self, api_client, create_admin_user1, create_nurse, create_rooms, create_shift_fixture,
                                 leave_create_fixture):
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        leave_id = leave[0].id
        data = data1["status_rejected_data"]

        url = reverse('all-leaves', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.put(url, data=data)
        assert response.status_code == 200


class TestGetLatestLeaves:
    @pytest.mark.django_db
    def test_get_latest_leave_requests(self, api_client, create_admin_user1, create_nurse, create_rooms,
                                       create_shift_fixture,
                                       leave_create_fixture):
        url = reverse('new-leaves')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200


class TestNeedSubstitutionView:
    @pytest.mark.django_db
    def test_get_leaves_to_substitute(self, api_client, create_admin_user1, create_nurse, create_rooms,
                                      create_shift_fixture,
                                      leave_create_fixture, approve_leave_fixture):
        url = reverse('leaves-accepted')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200


class TestAssignSubstituteView:
    @pytest.mark.django_db
    def test_assign_substitute1(self, api_client, create_admin_user1, create_nurse, create_nurse2, create_rooms,
                                create_nurse_shift_fixture,
                                leave_create_fixture, approve_leave_fixture):
        substitute = create_nurse2.email
        print(f'SUBSTITUTE-----{substitute}')
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(f'Leave    {leave[0].from_date}')
        print(f'Leave    {leave[0].to_date}')
        leave_id = leave[0].id
        data = {
            "for_date": "2022-12-28",
            "substitute": substitute
        }
        url = reverse('assign-substitute', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_assign_substitute2(self, api_client, create_admin_user1, create_nurse, create_nurse2, create_rooms,
                                create_nurse_shift_fixture,
                                leave_create_fixture, approve_leave_fixture):
        substitute = create_nurse2.email
        print(f'SUBSTITUTE-----{substitute}')
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(f'Leave    {leave[0].from_date}')
        print(f'Leave    {leave[0].to_date}')
        leave_id = leave[0].id
        data = {
            "for_date": "2022-12-25",
            "substitute": substitute
        }
        url = reverse('assign-substitute', kwargs={'pk': leave_id})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_assign_substitute3(self, api_client, create_admin_user1, create_nurse, create_nurse2, create_rooms,
                                create_nurse_shift_fixture,
                                leave_create_fixture, approve_leave_fixture):
        substitute = create_nurse2.email
        print(f'SUBSTITUTE-----{substitute}')
        employee_id = create_nurse.id
        leave = LeaveRequest.objects.filter(employee=employee_id)
        print(f'Leave    {leave[0].from_date}')
        print(f'Leave    {leave[0].to_date}')
        leave_id = leave[0].id
        data = {
            "for_date": "2022-12-25",
            "substitute": substitute
        }
        url = reverse('assign-substitute', kwargs={'pk': 2})
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.post(url, data=data)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_display_all_substitute(self, api_client, create_admin_user1, create_nurse, create_nurse2, create_rooms,
                                    create_nurse_shift_fixture,
                                    leave_create_fixture, approve_leave_fixture, assign_substitute_fixture):
        url = reverse('all-substitutes')
        api_client.force_authenticate(user=create_admin_user1)
        response = api_client.get(url)
        assert response.status_code == 200
