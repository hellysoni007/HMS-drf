from django.urls import path

from .views import PatientRegistrationView, ViewAvailableTimeSlots, ViewAllDoctors, BookAppointmentView, \
    UpdateAppointmentView, ShowTodaysAppointmentView, ShowAllAppointmentView, FilterDoctorAppointmentView, \
    CreateMedicationView, ShowMedicationView, UpdateMedicationView, ShowRegisteredPatientView, \
    UpdatePatientHealthDetails, ShowDoctorsAppointmentsView

urlpatterns = [
    path('', ShowRegisteredPatientView.as_view(), name="patient-registration-display"),  # DONE
    path('details/<int:pk>/', ShowRegisteredPatientView.as_view(), name="patient-registration"),  # DONE
    path('register/', PatientRegistrationView.as_view(), name="patient-registration"),  # DONE
    path('<int:pk>/update/', PatientRegistrationView.as_view(), name="update-patient"),  # DONE
    path('timeslots/', ViewAvailableTimeSlots.as_view(), name="time-slots"),  # DONE
    path('available-doctors/', ViewAllDoctors.as_view(), name="available-doctors"),  # DONE
    path('<int:pk>/book-appointment/', BookAppointmentView.as_view(), name="book-appointment"),  # DONE
    path('<int:pk>/update-appointment/<int:pk1>/', UpdateAppointmentView.as_view(), name="cancel-appointment"),  # DONE
    path('my-appointments/', ShowDoctorsAppointmentsView.as_view(), name="appointments-for-doctor"),  # DONE
    path('appointments/', ShowAllAppointmentView.as_view(), name="appointments"),  # DONE
    path('today-appointments/', ShowTodaysAppointmentView.as_view(), name="today-appointments"),  # DONE
    path('appointments/filter-by-doctor/', FilterDoctorAppointmentView.as_view(),
         name="filter-by"),  # Done
    path('medication/', CreateMedicationView.as_view(), name="medication"),  # DONE
    path('show-prescription/<int:patient_id>/', ShowMedicationView.as_view(), name="show-patients-prescription"),
    # DONE
    path('medication/add-medication/<int:id>/', UpdateMedicationView.as_view(),  # DONE
         name="add-medicines-to-prescription"),  # DONE
    path('medication/update-medication/<int:id1>/<int:id2>/', UpdateMedicationView.as_view(),
         name="update-medicine-in-prescription"),  # DONE
    path('medication/delete-medication/<int:id1>/<int:id2>/', UpdateMedicationView.as_view(),
         name="remove-medicine-from-prescription"),  # DONE
    path('<int:id>/update-profile/', UpdatePatientHealthDetails.as_view(), name="update-health-details"),  # DONE

]
