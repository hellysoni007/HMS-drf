from django.urls import path, include

from .views import UserRegistrationView, LoginView, UsersListView, ShiftCreateView, RoomCreateView, \
    UserDetailView, EmployeeShiftView, ViewProfileView, RoomUpdateView, \
    LeaveListCreateView, LeaveApprovalView, AssignSubstituteDuty, NeedSubstitution, GetLatestLeavesViews, \
    MonthlyScheduleView

urlpatterns = [
    path('login/', LoginView.as_view(), name="admin-login"),
    # Admin apis
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('users/', UsersListView.as_view(), name="view-all-users"),
    path('users/<int:pk>/', UserDetailView.as_view(), name="view-user-detail"),
    path('shifts/', ShiftCreateView.as_view(), name="view-shift"),
    path('shifts/<int:pk>/', ShiftCreateView.as_view(), name="update-shift"),
    path('rooms/', RoomCreateView.as_view(), name="add-room"),
    path('rooms/<int:pk>/', RoomUpdateView.as_view(), name="update-room"),
    path('profile/', ViewProfileView.as_view(), name="view-profile"),  # Update and view profile
    path('leaves/', LeaveApprovalView.as_view(), name="all-leaves"),
    path('leaves/<int:pk>/', LeaveApprovalView.as_view(), name="all-leaves"),
    path('new-leave-requests/', GetLatestLeavesViews.as_view(), name="new-leaves"),
    path('leaves-to-substitute/', NeedSubstitution.as_view(), name="leaves-accepted"),
    path('substitute/', AssignSubstituteDuty.as_view(), name="leaves-to-substitute"),
    path('assign-substitute/<int:pk>/', AssignSubstituteDuty.as_view(), name="leaves-substitute"),


    # All employees apis
    path('my-shift/', EmployeeShiftView.as_view(), name="view-shift"),
    path('my-schedule/', MonthlyScheduleView.as_view(), name="view-schedule"),
    path('my-leaves/', LeaveListCreateView.as_view(), name="my-leaves"),
    path('my-leaves/<int:pk>/', LeaveListCreateView.as_view(), name="my-leaves"),

    # Receptionist apis
    path('add-patients/', include('patients.urls'), name="add-patients"),



    # path('view-all-patients/', PatientListView.as_view(), name="view-all-patients"),

]
