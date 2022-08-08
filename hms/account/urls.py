from django.urls import path

from .views import UserRegistrationView, LoginView, UsersListView, ShiftCreateView, RoomCreateView, \
    PatientCreateView, UserDetailView, EmployeeShiftView, ViewProfileView, ScheduleView

urlpatterns = [
    path('login/', LoginView.as_view(), name="admin-login"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('view-all-users/   ', UsersListView.as_view(), name="view-all-users"),
    path('view-all-users/<int:pk>/', UserDetailView.as_view(), name="view-all-users"),

    path('update-shift/<int:pk>/', ShiftCreateView.as_view(), name="update-shift"),
    path('view-shift/', EmployeeShiftView.as_view(), name="view-shift"),
    path('add-room/', RoomCreateView.as_view(), name="add-room"),
    path('add-patients/', PatientCreateView.as_view(), name="add-patients"),
    path('view-profile/', ViewProfileView.as_view(), name="view-profile"),
    path('update-profile/', ViewProfileView.as_view(), name="update-profile"),
    path('view-schedule/', ScheduleView.as_view(), name="view-schedule"),

    # path('view-all-patients/', PatientListView.as_view(), name="view-all-patients"),

]
