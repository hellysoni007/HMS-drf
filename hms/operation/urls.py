from django.urls import path

from operation.views import DisplayBedsView, DisplayAvailableBedsView, CreateUpdateBedView, DeleteBedView, \
    UpdateBedAvailabilityView, ScheduleOperationView, ShowOperationsView, UpdateOperationDetailView, \
    ShowTodayOperationView, ShowDoctorOperationView, ShowTodayDoctorOperationView, CreatePatientAdmissionDetailsView, \
    DisplayCurrentlyAdmittedPatientsView, DisplayAllAdmittedPatientsView, \
    UpdatePatientAdmissionDetailsView, DisplayAvailableOTTimeslots, DisplayAvailableSurgeons, CreateDoctorVisitView, \
    CreateNurseVisitView, PatientVisitView, DisplayScheduledPatientOperationView, DisplayAllPatientOperationView, \
    ShowDoctorListOperationView, ShowDoctorListOperationTodayView, ShowPatientAdmissionDetailsView
from patients.views import ShowRegisteredPatientView

urlpatterns = [
    path('', ShowOperationsView.as_view(), name="view-all-operations"),  # Done
    path('<int:op_id>/update/', UpdateOperationDetailView.as_view(), name="update-operations-detail"),  # Done
    path('today/', ShowTodayOperationView.as_view(), name="view-todays-operations"),  # Done
    path('<int:doctor_id>/', ShowDoctorOperationView.as_view(), name="view-doctors-operations"),  # Done
    path('<int:doctor_id>/today/', ShowTodayDoctorOperationView.as_view(), name="view-doctors-operations"),  # Done
    path('my-operations/', ShowDoctorListOperationView.as_view(), name="view-my-operations"),  # Done
    path('my-operations/today/', ShowDoctorListOperationTodayView.as_view(), name="view-my-operations-today"),  # Done

    path('patients/', ShowRegisteredPatientView.as_view(), name="show-patients"),  # Done
    path('patients/<int:pk>', ShowRegisteredPatientView.as_view(), name="show-patients"),  # Done
    path('patients/<int:patient_id>/schedule-operation/', ScheduleOperationView.as_view(),
         name="schedule-operation"),  # Done

    path('available-surgeons/', DisplayAvailableSurgeons.as_view(), name="view-available-surgeons"),  # Done

    path('beds/', DisplayBedsView.as_view(), name="view-all-beds"),  # Done
    path('beds/create/', CreateUpdateBedView.as_view(), name="add-bed"),  # Done
    path('beds/<int:id>/update/', CreateUpdateBedView.as_view(), name="update-bed"),  # Done
    path('beds/<int:id>/update-availability/', UpdateBedAvailabilityView.as_view(), name="update-bed-availability"),
    # Done
    path('beds/<int:id>/delete/', DeleteBedView.as_view(), name="delete-bed"),  # Done
    path('beds/<int:id>/', DisplayBedsView.as_view(), name="view-beds-detail"),  # Done
    path('beds/available/', DisplayAvailableBedsView.as_view(), name="view-available-beds"),  # Done

    path('available-timeslots/', DisplayAvailableOTTimeslots.as_view(), name="view-available-timeslots"),  # Done

    path('admit-patient/create/', CreatePatientAdmissionDetailsView.as_view(),
         name="create-update-admit-patient"),  # Done
    path('admit-patient/<int:admission_id>/', ShowPatientAdmissionDetailsView.as_view(),
         name="view-admissions-detail"),  # Done
    path('admit-patient/<int:admission_id>/update', UpdatePatientAdmissionDetailsView.as_view(),
         name="update-admit-patient-discharge-date"),  # Done
    path('admit-patient/all/', DisplayAllAdmittedPatientsView.as_view(), name="view-all-admissions"),  # Done
    path('admit-patient/', DisplayCurrentlyAdmittedPatientsView.as_view(), name="view-active-admissions"),  # Done

    path('scheduled/', DisplayScheduledPatientOperationView.as_view(), name="view-patients-Op-scheduled"),  # Done
    path('scheduled/<int:patient_id>/', DisplayScheduledPatientOperationView.as_view(),  # Done
         name="view-patients-Op-scheduled-details"),
    path('patient/', DisplayAllPatientOperationView.as_view(), name="view-patients-Op-all"),  # Done
    path('patient/<int:patient_id>/', DisplayAllPatientOperationView.as_view(),  # Done
         name="view-patients-Op-all-details"),

    path('patient/<int:patient_id>/post-op-visits/', PatientVisitView.as_view(), name="view-post-op-visits"),  # Done

    # Post Op details nurse
    path('patient/post-op-visits/nurse/', CreateNurseVisitView.as_view(),
         name="show-nurse-visit-details"),  # view nurse visits  # Done
    path('patient/<int:patient_id>/post-op-visits/nurse/create/', CreateNurseVisitView.as_view(),
         name="add-nurse-visit-details"),  # nurse updates  # Done

    # Post Op details doctor
    path('patient/post-op-visits/doctor/', CreateDoctorVisitView.as_view(),
         name="show-visit-details"),  # view doctors visits # Done
    path('patient/<int:patient_id>/post-op-visits/doctor/create/', CreateDoctorVisitView.as_view(),
         name="add-visit-details"),  # Done

]
