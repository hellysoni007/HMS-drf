from django.urls import path

from .views import UserRegistrationView, LoginView, UsersListView, ShiftCreateView, RoomCreateView, \
    UserDetailView, EmployeeShiftView, ViewProfileView, RoomUpdateView, \
    LeaveListCreateView, LeaveApprovalView, AssignSubstituteDuty, NeedSubstitution, GetLatestLeavesViews, \
    MonthlyScheduleView, LeaveDeleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name="admin-login"),  # Done
    # Admin apis
    path('register/', UserRegistrationView.as_view(), name="register"),  # Done
    path('users/', UsersListView.as_view(), name="view-all-users"),  # Done
    path('users/<int:pk>/', UserDetailView.as_view(), name="view-user-detail"),  # Done
    path('shifts/', ShiftCreateView.as_view(), name="create-shift"),  # Done
    path('shifts/<int:pk>/', ShiftCreateView.as_view(), name="update-shift"),  # Done
    path('rooms/', RoomCreateView.as_view(), name="add-room"),  # Done
    path('rooms/<int:pk>/', RoomUpdateView.as_view(), name="update-room"),  # Done
    path('profile/', ViewProfileView.as_view(), name="view-profile"),  # Done
    path('leaves/', LeaveApprovalView.as_view(), name="all-leaves"),  # Done
    path('leaves/<int:pk>/', LeaveApprovalView.as_view(), name="all-leaves"),  # Done
    path('new-leave-requests/', GetLatestLeavesViews.as_view(), name="new-leaves"),  # Done
    path('leaves-to-substitute/', NeedSubstitution.as_view(), name="leaves-accepted"),  # Done
    path('substitute/', AssignSubstituteDuty.as_view(), name="leaves-to-substitute"),  # Done
    path('assign-substitute/<int:pk>/', AssignSubstituteDuty.as_view(), name="leaves-substitute"),  # Done

    # All employees apis
    path('my-shift/', EmployeeShiftView.as_view(), name="view-shift"),  # DONE
    path('my-schedule/', MonthlyScheduleView.as_view(), name="view-schedule"),  # DONE
    path('my-leaves/', LeaveListCreateView.as_view(), name="my-leaves"),  # Done
    path('my-leaves/<int:pk>/', LeaveListCreateView.as_view(), name="my-leaves"),  # Done
    path('my-leaves/<int:pk>/delete/', LeaveDeleteView.as_view(), name="delete-leave"),  # Done
]
