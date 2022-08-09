from django.urls import path

from .views import UserRegistrationView, LoginView, UsersListView, ShiftCreateView, RoomCreateView, \
    PatientCreateView, UserDetailView, EmployeeShiftView, ViewProfileView, ScheduleView,RoomUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name="admin-login"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('users/', UsersListView.as_view(), name="view-all-users"),
    path('users/<int:pk>/', UserDetailView.as_view(), name="view-user-detail"),
    path('shifts/', ShiftCreateView.as_view(), name="view-shift"),
    path('shifts/<int:pk>/', ShiftCreateView.as_view(), name="update-shift"),
    path('my-shift/', EmployeeShiftView.as_view(), name="view-shift"),
    path('rooms/', RoomCreateView.as_view(), name="add-room"),
    path('rooms/<int:pk>/', RoomUpdateView.as_view(), name="update-room"),
    path('add-patients/', PatientCreateView.as_view(), name="add-patients"),
    path('profile/', ViewProfileView.as_view(), name="view-profile"),
    path('update-profile/', ViewProfileView.as_view(), name="update-profile"),
    path('my-schedule/', ScheduleView.as_view(), name="view-schedule"),

    # path('view-all-patients/', PatientListView.as_view(), name="view-all-patients"),

]
