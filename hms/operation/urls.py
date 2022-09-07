from django.urls import path

from operation.views import DisplayBedsView, DisplayAvailableBedsView, CreateUpdateBedView, DeleteBedView, \
    UpdateBedAvailabilityView, ScheduleOperationView, ShowOperationsView, UpdateOperationDetailView, \
    ShowTodayOperationView, ShowDoctorOperationView, ShowTodayDoctorOperationView, CreatePatientAdmissionDetailsView, \
    DisplayCurrentlyAdmittedPatientsView, DisplayAllAdmittedPatientsView, \
    UpdatePatientAdmissionDetailsView, DisplayAvailableOTTimeslots, DisplayAvailableSurgeons, CreateDoctorVisitView, \
    CreateNurseVisitView, PatientVisitView, DisplayScheduledPatientOperationView, DisplayAllPatientOperationView, \
    ShowDoctorListOperationView, ShowDoctorListOperationTodayView
from patients.views import ShowRegisteredPatientView

urlpatterns = [
    path('', ShowOperationsView.as_view(), name="view-all-operations"),
    path('<int:op_id>/update/', UpdateOperationDetailView.as_view(), name="update-operations-detail"),
    path('today/<int:id>', ShowTodayOperationView.as_view(), name="view-todays-operations"),
    path('<int:doctor_id>/', ShowDoctorOperationView.as_view(), name="view-doctors-operations"),
    path('<int:doctor_id>/today/', ShowTodayDoctorOperationView.as_view(), name="view-doctors-operations"),
    path('my-operations/', ShowDoctorListOperationView.as_view(), name="view-my-operations"),
    path('my-operations/today/', ShowDoctorListOperationTodayView.as_view(), name="view-my-operations-today"),

    path('patients/', ShowRegisteredPatientView.as_view(), name="show-patients"),
    path('patients/<int:patient_id>/schedule-operation/', ScheduleOperationView.as_view(), name="schedule-operation"),

    path('available-surgeons/', DisplayAvailableSurgeons.as_view(), name="view-available-surgeons"),

    path('beds/', DisplayBedsView.as_view(), name="view-all-beds"),
    path('beds/create/', CreateUpdateBedView.as_view(), name="add-bed"),
    path('beds/<int:id>/update', CreateUpdateBedView.as_view(), name="update-bed"),
    path('beds/<int:id>/update-availability/', UpdateBedAvailabilityView.as_view(), name="update-bed"),
    path('beds/<int:id>/delete', DeleteBedView.as_view(), name="update-bed"),
    path('beds/<int:id>/', DisplayBedsView.as_view(), name="view-beds-detail"),
    path('beds/available/', DisplayAvailableBedsView.as_view(), name="view-available-beds"),
    path('beds/available/?<int:bed_id>', DisplayAvailableBedsView.as_view(), name="view-bed-detail"),

    path('available-timeslots/', DisplayAvailableOTTimeslots.as_view(), name="view-available-timeslots"),

    path('admit-patient/create/', CreatePatientAdmissionDetailsView.as_view(),
         name="create-update-admit-patient"),
    path('admit-patient/<int:admission_id>/', UpdatePatientAdmissionDetailsView.as_view(),
         name="view-admissions-detail"),
    path('admit-patient/<int:admission_id>/update', UpdatePatientAdmissionDetailsView.as_view(),
         name="update-admit-patient"),
    path('admit-patient/all/', DisplayAllAdmittedPatientsView.as_view(), name="view-all-admissions"),
    path('admit-patient/', DisplayCurrentlyAdmittedPatientsView.as_view(), name="view-active-admissions"),

    path('patient/', DisplayScheduledPatientOperationView.as_view(), name="view-patients-Op-scheduled"),
    path('patient/<int:patient_id>/', DisplayScheduledPatientOperationView.as_view(),
         name="view-patients-Op-scheduled-details"),
    path('patient/', DisplayAllPatientOperationView.as_view(), name="view-patients-Op-all"),
    path('patient/<int:patient_id>/', DisplayAllPatientOperationView.as_view(),
         name="view-patients-Op-all-details"),


    path('patient/<int:patient_id>/post-op-visits/', PatientVisitView.as_view(), name="view-post-op-visits"),

    # Post Op details nurse
    path('patient/<int:patient_id>/post-op-visits/nurse/', CreateNurseVisitView.as_view(),
         name="show-nurse-visit-details"),  # view nurse visits
    path('patient/<int:patient_id>/post-op-visits/nurse/create/', CreateNurseVisitView.as_view(),
         name="add-nurse-visit-details"),  # nurse updates

    # Post Op details doctor
    path('patient/<int:patient_id>/post-op-visits/doctor/', CreateDoctorVisitView.as_view(),
         name="show-visit-details"),  # view doctors visits
    path('patient/<int:patient_id>/post-op-visits/doctor/create/', CreateDoctorVisitView.as_view(),
         name="add-visit-details"),



]
