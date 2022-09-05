from django.urls import path

from operation.views import DisplayBedsView, DisplayAvailableBedsView, CreateUpdateBedView, DeleteBedView, \
    UpdateBedAvailabilityView, ScheduleOperationView, ShowOperationsView, UpdateOperationDetailView, \
    ShowTodayOperationView, ShowDoctorOperationView, ShowTodayDoctorOperationView, CreatePatientAdmissionDetailsView, \
    DisplayCurrentlyAdmittedPatientsView, DisplayAllAdmittedPatientsView, \
    ListUpdatePatientAdmissionDetailsView
from patients.views import ShowRegisteredPatientView

urlpatterns = [
    path('', ShowOperationsView.as_view(), name="view-all-operations"),
    path('<int:op_id>/update/', UpdateOperationDetailView.as_view(), name="update-operations-detail"),
    path('today/<int:id>', ShowTodayOperationView.as_view(), name="view-todays-operations"),
    path('<int:doctor_id>/', ShowDoctorOperationView.as_view(), name="view-doctors-operations"),
    path('<int:doctor_id>/today/', ShowTodayDoctorOperationView.as_view(), name="view-doctors-operations"),

    path('patients/', ShowRegisteredPatientView.as_view(), name="show-patients"),
    path('patients/<int:patient_id>/schedule-operation/', ScheduleOperationView.as_view(), name="schedule-operation"),

    # path('available-surgeons/', name="view-available-surgeons"),

    path('beds/', DisplayBedsView.as_view(), name="view-all-beds"),
    path('beds/create/', CreateUpdateBedView.as_view(), name="add-bed"),
    path('beds/<int:id>/update', CreateUpdateBedView.as_view(), name="update-bed"),
    path('beds/<int:id>/update-availability/', UpdateBedAvailabilityView.as_view(), name="update-bed"),
    path('beds/<int:id>/delete', DeleteBedView.as_view(), name="update-bed"),
    path('beds/<int:id>/', DisplayBedsView.as_view(), name="view-beds-detail"),
    path('beds/available/', DisplayAvailableBedsView.as_view(), name="view-available-beds"),
    path('beds/available/?<int:bed_id>', DisplayAvailableBedsView.as_view(), name="view-bed-detail"),

    # path('available-timeslots/', name="view-available-timeslots"),
    # path('available-timeslots/<int:timeslot_id>', name="view-available-timeslots-detail"),

    path('admit-patient/<int:patient_id>/', CreatePatientAdmissionDetailsView.as_view(),
         name="create-update-admit-patient"),
    path('admissions/<int:admission_id>/', ListUpdatePatientAdmissionDetailsView.as_view(),
         name="view-admissions-detail"),
    path('admit-patient/<int:admission_id>/update', ListUpdatePatientAdmissionDetailsView.as_view(),
         name="update-admit-patient"),
    path('admissions/all/', DisplayAllAdmittedPatientsView.as_view(), name="view-all-admissions"),
    path('admissions/', DisplayCurrentlyAdmittedPatientsView.as_view(), name="view-active-admissions"),

]
