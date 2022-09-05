from django.urls import path

from .views import PatientRegistrationView, ViewAvailableTimeSlots, ViewAllDoctors, BookAppointmentView, \
    UpdateAppointmentView, ShowTodaysAppointmentView, ShowAllAppointmentView, FilterDoctorAppointmentView, \
    CreateMedicationView, ShowMedicationView, UpdateMedicationView, ShowRegisteredPatientView, \
    UpdatePatientHealthDetails, ShowDoctorsAppointmentsView

urlpatterns = [
    path('', ShowRegisteredPatientView.as_view(), name="patient-registration-display"),
    path('details/<int:pk>/', ShowRegisteredPatientView.as_view(), name="patient-registration"),
    path('register/', PatientRegistrationView.as_view(), name="patient-registration"),
    path('<int:pk>/', PatientRegistrationView.as_view(), name="update-patient"),
    path('timeslots/', ViewAvailableTimeSlots.as_view(), name="time-slots"),
    path('available-doctors/', ViewAllDoctors.as_view(), name="available-doctors"),
    path('<int:pk>/book-appointment/', BookAppointmentView.as_view(), name="book-appointment"),
    path('<int:pk>/update-appointment/<int:pk1>/', UpdateAppointmentView.as_view(), name="book-appointment"),
    path('my-appointments/', ShowDoctorsAppointmentsView.as_view(), name="appointments"),
    path('appointments/', ShowAllAppointmentView.as_view(), name="appointments"),
    path('today-appointments/', ShowTodaysAppointmentView.as_view(), name="today-appointments"),
    path('appointments/filter-by-doctor/', FilterDoctorAppointmentView.as_view(),
         name="filter-by"),
    path('medication/', CreateMedicationView.as_view(), name="medication"),
    path('show-prescription/<int:patient_id>/', ShowMedicationView.as_view(), name="show-patients-prescription"),
    path('medication/add-medication/<int:id>/', UpdateMedicationView.as_view(), name="add-medicines-to-prescription"),
    path('medication/update-medication/<int:id1>/<int:id2>/', UpdateMedicationView.as_view(),
         name="update-medicine-in-prescription"),
    path('medication/delete-medication/<int:id1>/<int:id2>/', UpdateMedicationView.as_view(),
         name="remove-medicine-from-prescription"),
    path('<int:id>/update-profile/', UpdatePatientHealthDetails.as_view(), name="update-health-details"),

]
