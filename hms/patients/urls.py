from django.urls import path

from .views import PatientRegistrationView, ViewAvailableTimeSlots, ViewAllDoctors, BookAppointmentView, \
    UpdateAppointmentView, ShowTodaysAppointmentView, ShowAllAppointmentView, FilterDoctorsAppointmentView

urlpatterns = [
    path('', PatientRegistrationView.as_view(), name="patient-registration"),
    path('register/', PatientRegistrationView.as_view(), name="patient-registration"),
    path('<int:pk>/', PatientRegistrationView.as_view(), name="patient-registration"),
    path('timeslots/', ViewAvailableTimeSlots.as_view(), name="time-slots"),
    path('available-doctors/', ViewAllDoctors.as_view(), name="available-doctors"),
    path('<int:pk>/book-appointment/', BookAppointmentView.as_view(), name="book-appointment"),
    path('<int:pk>/update-appointment/<int:pk1>/', UpdateAppointmentView.as_view(), name="book-appointment"),
    path('appointments/', ShowAllAppointmentView.as_view(), name="appointments"),
    path('today-appointments/', ShowTodaysAppointmentView.as_view(), name="today-appointments"),
    path('appointments/filter-by-doctor/', FilterDoctorsAppointmentView.as_view(), name="filter-by"),
]
