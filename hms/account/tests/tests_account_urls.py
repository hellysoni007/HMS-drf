import pytest
from django.urls import reverse, resolve

import account


@pytest.mark.django_db
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_login_url(api_client):
    url = reverse("admin-login")
    assert resolve(url).func.view_class == account.views.LoginView


@pytest.mark.django_db
def test_register_url(api_client):
    url = reverse("register")
    assert resolve(url).func.view_class == account.views.UserRegistrationView


@pytest.mark.django_db
def test_view_all_users_url(api_client):
    url = reverse("view-all-users")
    assert resolve(url).func.view_class == account.views.UsersListView


@pytest.mark.django_db
def test_view_user_detail_url(api_client):
    url = reverse("view-user-detail", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.UserDetailView


@pytest.mark.django_db
def test_create_shift_url(api_client):
    url = reverse("create-shift", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.ShiftCreateView


@pytest.mark.django_db
def test_update_shift_url(api_client):
    url = reverse("update-shift")
    assert resolve(url).func.view_class == account.views.ShiftCreateView


@pytest.mark.django_db
def test_update_shift_detail_url(api_client):
    url = reverse("update-shift", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.ShiftCreateView


@pytest.mark.django_db
def test_add_room_url(api_client):
    url = reverse("add-room")
    assert resolve(url).func.view_class == account.views.RoomCreateView


@pytest.mark.django_db
def test_update_room_url(api_client):
    url = reverse("update-room", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.RoomUpdateView


@pytest.mark.django_db
def test_view_profile_url(api_client):
    url = reverse("view-profile")
    assert resolve(url).func.view_class == account.views.ViewProfileView


@pytest.mark.django_db
def test_all_leaves_url(api_client):
    url = reverse("all-leaves")
    assert resolve(url).func.view_class == account.views.LeaveApprovalView


@pytest.mark.django_db
def test_all_leaves_details_url(api_client):
    url = reverse("all-leaves", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.LeaveApprovalView


@pytest.mark.django_db
def test_latest_leaves_details_url(api_client):
    url = reverse("new-leaves")
    assert resolve(url).func.view_class == account.views.GetLatestLeavesViews


@pytest.mark.django_db
def test_accepted_leaves_details_url(api_client):
    url = reverse("leaves-accepted")
    assert resolve(url).func.view_class == account.views.NeedSubstitution


@pytest.mark.django_db
def test_all_substitutes_url(api_client):
    url = reverse("all-substitutes")
    assert resolve(url).func.view_class == account.views.AssignSubstituteDuty


@pytest.mark.django_db
def test_assign_substitute_url(api_client):
    url = reverse("assign-substitute", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.AssignSubstituteDuty


@pytest.mark.django_db
def test_view_shift_url(api_client):
    url = reverse("view-shift")
    assert resolve(url).func.view_class == account.views.EmployeeShiftView


@pytest.mark.django_db
def test_view_schedule_url(api_client):
    url = reverse("view-schedule")
    assert resolve(url).func.view_class == account.views.MonthlyScheduleView


@pytest.mark.django_db
def test_my_leaves_url(api_client):
    url = reverse("my-leaves")
    assert resolve(url).func.view_class == account.views.LeaveListCreateView


@pytest.mark.django_db
def test_my_leaves_details_url(api_client):
    url = reverse("my-leaves", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.LeaveListCreateView


@pytest.mark.django_db
def test_delete_leave_url(api_client):
    url = reverse("delete-leave", kwargs={'pk': 1})
    assert resolve(url).func.view_class == account.views.LeaveDeleteView
