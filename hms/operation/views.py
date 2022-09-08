from rest_framework import generics
from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse, IsAdmin
from operation.services import ManageBedService, ManageTimeSlotsOTService, ManageOperationsService, \
    ManagePatientAdmissionService, ManageSurgeonAvailabilityService, ManagePatientVisitsService, ManagePatientDetails


class CreateUpdateBedView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        new_bed = ManageBedService.add_new_bed(request)
        return new_bed

    def put(self, request, *args, **kwargs):
        update_bed = ManageBedService.update_existing_bed(kwargs, request)
        return update_bed


class UpdateBedAvailabilityView(generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def put(self, request, *args, **kwargs):
        update_availability = ManageBedService.update_existing_bed_availability(kwargs, request)
        return update_availability


class DeleteBedView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]

    def delete(self, request, *args, **kwargs):
        delete_bed = ManageBedService.delete_existing_bed(kwargs)
        return delete_bed


class DisplayBedsView(generics.ListAPIView):
    permission_classes = [IsAdmin | IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        display_bed = ManageBedService.show_all_beds(kwargs)
        return display_bed


# View available beds
class DisplayAvailableBedsView(generics.ListAPIView):
    permission_classes = [IsAdmin | IsReceptionist]

    def get(self, request, *args, **kwargs):
        if self.request.query_params:
            bed_id = self.request.query_params['bed_id']
        else:
            bed_id = None
        available_beds = ManageBedService.show_available_beds(bed_id)
        return available_beds


# Operation views

# Schedule Operation
class ScheduleOperationView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        new_operation = ManageOperationsService.schedule_operations(kwargs, request)
        return new_operation


# Show all operations and view operation details
class ShowOperationsView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):

        if self.request.query_params:
            op_id = int(self.request.query_params['op_id'])
            print(type(op_id))
        else:
            op_id = None
        operations = ManageOperationsService.get_all_operations_details(op_id)
        return operations


class ShowTodayDoctorOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs['doctor_id']
        if self.request.query_params:
            op_id = self.request.query_params['op_id']
        else:
            op_id = None
        today_operations = ManageOperationsService.filter_operations_by_doctor_today(op_id, doctor_id)
        return today_operations


# Filter Operations by doctor
class ShowDoctorOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs['doctor_id']
        if self.request.query_params:
            op_id = self.request.query_params['op_id']
        else:
            op_id = None
        operations = ManageOperationsService.filter_operations_by_doctor(op_id, doctor_id)
        return operations


class ShowDoctorListOperationView(generics.ListAPIView):
    permission_classes = [IsSurgeon | IsDoctor]

    def get(self, request, *args, **kwargs):
        doctor_id = request.user.id
        if self.request.query_params:
            op_id = self.request.query_params['op_id']
        else:
            op_id = None
        operations = ManageOperationsService.show_my_operations(op_id, doctor_id)
        return operations


class ShowDoctorListOperationTodayView(generics.ListAPIView):
    permission_classes = [IsSurgeon | IsDoctor]

    def get(self, request, *args, **kwargs):
        doctor_id = request.user.id
        if self.request.query_params:
            op_id = self.request.query_params['op_id']
        else:
            op_id = None
        operations = ManageOperationsService.show_my_operations_today(op_id, doctor_id)
        return operations


class ShowTodayOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        if self.request.query_params:
            op_id = self.request.query_params['op_id']
        else:
            op_id = None
        operations = ManageOperationsService.get_all_operations_today_details(op_id)
        return operations


class UpdateOperationDetailView(generics.UpdateAPIView):
    permission_classes = [IsSurgeon]

    def put(self, request, *args, **kwargs):
        update_status = ManageOperationsService.update_operation_status(kwargs, request)
        return update_status


class CreatePatientAdmissionDetailsView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        new_admission = ManagePatientAdmissionService.new_patient_admission(request)
        return new_admission


class UpdatePatientAdmissionDetailsView(generics.UpdateAPIView):
    permission_classes = [IsSurgeon | IsDoctor]

    def put(self, request, *args, **kwargs):
        update_admission = ManagePatientAdmissionService.update_patient_admission(kwargs, request)
        return update_admission


class ShowPatientAdmissionDetailsView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse | IsAdmin]

    def get(self, request, *args, **kwargs):
        admission_details = ManagePatientAdmissionService.get_patient_admission_details(kwargs)
        return admission_details


class DisplayCurrentlyAdmittedPatientsView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse | IsAdmin]

    def get(self, request, *args, **kwargs):
        admitted_patient = ManagePatientAdmissionService.get_currently_admitted_patients()
        return admitted_patient


class DisplayAllAdmittedPatientsView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse | IsAdmin]

    def get(self, request, *args, **kwargs):
        admitted_patient = ManagePatientAdmissionService.get_all_admitted_patients()
        return admitted_patient


class DisplayAvailableOTTimeslots(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        available_timeslots = ManageTimeSlotsOTService.get_available_timeslots(request)
        return available_timeslots
        # pass


class DisplayAvailableSurgeons(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        surgeons = ManageSurgeonAvailabilityService.get_available_surgeon()
        return surgeons


class CreateNurseVisitView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [IsNurse]

    def post(self, request, *args, **kwargs):
        print(request.user.role)
        add_visit = ManagePatientVisitsService.add_visit_nurse(kwargs, request)
        return add_visit

    def get(self, request, *args, **kwargs):
        get_visit_details = ManagePatientVisitsService.get_nurse_visit_details(request)
        return get_visit_details


class CreateDoctorVisitView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [IsSurgeon | IsDoctor]

    def post(self, request, *args, **kwargs):
        add_visit_data = ManagePatientVisitsService.add_doctor_visit(kwargs, request)
        return add_visit_data

    def get(self, request, *args, **kwargs):
        visit_data = ManagePatientVisitsService.get_doctor_visit_details(request)
        return visit_data


class PatientVisitView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        visits = ManagePatientVisitsService.get_visit_details_by_patient(kwargs)
        return visits


class DisplayScheduledPatientOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        operations = ManageOperationsService.get_scheduled_operations(kwargs)
        return operations


class DisplayAllPatientOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        patient_details = ManagePatientDetails.get_operation_details(kwargs)
        return patient_details
