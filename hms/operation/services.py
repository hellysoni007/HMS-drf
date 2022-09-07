import datetime

from rest_framework import status
from rest_framework.response import Response

from account.models import Shifts, User
from operation.models import Bed, Operation, Admission, NurseVisit, DoctorsVisit
from operation.serializers import CreateBedSerializer, UpdateBedSerializer, UpdateBedAvailabilitySerializer, \
    DisplayBedSerializer, ScheduleOperationSerializer, ShowAllOperationsSerializer, UpdateOperationsSerializer, \
    CreatePatientAdmissionSerializer, UpdatePatientAdmissionSerializer, DisplayPatientAdmissionsSerializer, \
    CreateNurseVisitSerializer, CreateDoctorsVisitSerializer, ViewPatientOperationSerializer
from patients.models import TimeSlots, PatientProfile
from patients.serializers import ViewAvailableTimeSlotsSerializer, ViewAvailableDoctorsSerializer


class ManageBedService:
    @staticmethod
    def add_new_bed(request):
        serializer = CreateBedSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Bed added successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_existing_bed(kwargs, request):
        bed_id = kwargs['id']
        try:
            queryset = Bed.objects.get(id=bed_id)
        except Bed.DoesNotExist:
            return Response({'msg': 'Bed not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateBedSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Bed updated successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_existing_bed_availability(kwargs, request):
        bed_id = kwargs['id']
        try:
            queryset = Bed.objects.get(id=bed_id)
        except Bed.DoesNotExist:
            return Response({'msg': 'Bed not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateBedAvailabilitySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Bed availability updated successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_existing_bed(kwargs):
        bed_id = kwargs['id']
        try:
            bed = Bed.objects.get(id=bed_id)
            if not bed.is_available:
                return Response({'msg': 'Bed is occupied. Cannot remove bed'},
                                status=status.HTTP_404_NOT_FOUND)
            bed.is_delete = True
            bed.save()
        except Bed.DoesNotExist:
            return Response({'msg': 'Bed not found'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'Bed deleted successfully'},
                        status=status.HTTP_200_OK)

    @staticmethod
    def show_all_beds(kwargs):
        if kwargs:
            bed_id = kwargs['id']
            queryset = Bed.objects.filter(id=bed_id).exclude(is_delete=True)
            if not queryset:
                return Response({'msg': 'Bed not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Bed.objects.all().exclude(is_delete=True)
        serializer = DisplayBedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def show_available_beds(bed_id):
        if bed_id:
            queryset = Bed.objects.filter(id=bed_id, is_available=True).exclude(is_delete=True)
            if not queryset:
                return Response({'msg': 'Bed not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Bed.objects.filter(is_available=True, is_delete=False)
        serializer = DisplayBedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageTimeSlotsOTService:
    @staticmethod
    def get_available_timeslots(request):
        operations = Operation.objects.filter(date=request.data['check-date'], status="SCHEDULED",
                                              doctor=request.data['doctor'])
        print(operations)
        booked_timeslots = []
        for operation in operations:
            booked_timeslots.append(operation.timeslot.id)
        queryset = TimeSlots.objects.all().exclude(id__in=booked_timeslots).exclude(id__in=[i for i in range(1, 31)])
        serializer = ViewAvailableTimeSlotsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageOperationsService:
    @staticmethod
    def schedule_operations(kwargs, request):
        patient_id = kwargs['patient_id']
        try:
            patient_profile = PatientProfile.objects.get(patient_id=patient_id)
            if patient_profile.advise != 'Operation':
                return Response({'error-msg': 'Patient is not advised for operation.'}, status=status.HTTP_201_CREATED)
        except PatientProfile.DoesNotExist:
            return Response({'error-msg': 'Invalid patient Id.'}, status=status.HTTP_201_CREATED)

        request.data['patient'] = patient_id
        serializer = ScheduleOperationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status='SCHEDULED')
            return Response({'msg': 'Operation scheduled successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_scheduled_operations(kwargs):
        operations = Operation.objects.filter(status='SCHEDULED')
        patients = operations.values('patient')
        users = User.objects.filter(id__in=patients)
        if kwargs:
            patient_id = kwargs['patient_id']
            users = users.filter(id=patient_id)
            if not users:
                return Response(
                    {'error-msg': 'Patient is not operated or'},
                    status=status.HTTP_404_NOT_FOUND)
        serializer = ViewPatientOperationSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    @staticmethod
    def get_all_operations_details(op_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            queryset = Operation.objects.all().order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_all_operations_today_details(op_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            today = datetime.date.today()
            queryset = Operation.objects.filter(date=today)
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def filter_operations_by_doctor_today(op_id, doctor_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            today = datetime.date.today()
            queryset = Operation.objects.filter(doctor=doctor_id, date=today)
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def filter_operations_by_doctor(op_id, doctor_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            queryset = Operation.objects.filter(doctor=doctor_id).order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def show_my_operations(op_id, doctor_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            queryset = Operation.objects.filter(doctor=doctor_id).order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def show_my_operations_today(op_id, doctor_id):
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            today = datetime.date.today()
            queryset = Operation.objects.filter(doctor=doctor_id, date=today).order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def update_operation_status(kwargs, request):
        op_id = kwargs['op_id']
        try:
            queryset = Operation.objects.get(id=op_id)
        except Operation.DoesNotExist:
            return Response({'error-msg': 'Invalid Operation ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateOperationsSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Operation status updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagePatientAdmissionService:

    @staticmethod
    def new_patient_admission(request):
        serializer = CreatePatientAdmissionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Operation scheduled successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_patient_admission(kwargs, request):
        queryset = Admission.objects.get(id=kwargs['admission_id'])
        serializer = UpdatePatientAdmissionSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient admission details updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_patient_admission_details(kwargs):
        try:
            queryset = Admission.objects.get(id=kwargs['admission_id'])
        except Admission.DoesNotExist:
            return Response({'error-msg': 'Invalid Admission Id.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DisplayPatientAdmissionsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_currently_admitted_patients():
        today = datetime.date.today()
        queryset = Admission.objects.filter(discharge_date__gte=today)
        serializer = DisplayPatientAdmissionsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_all_admitted_patients():
        queryset = Admission.objects.all().order_by('discharge_date', 'admission_date')
        serializer = DisplayPatientAdmissionsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageSurgeonAvailabilityService:

    @staticmethod
    def get_available_surgeon():
        queryset = Shifts.objects.filter(allocated_place="OT")
        serializer = ViewAvailableDoctorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagePatientVisitsService:

    @staticmethod
    def add_visit_nurse(kwargs, request):
        patient_id = kwargs['patient_id']
        request.data['patient'] = patient_id
        request.data['nurse'] = request.user.id
        operation = Operation.objects.get(patient=patient_id)
        surgeon = operation.doctor
        request.data['surgeon'] = surgeon.id

        serializer = CreateNurseVisitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Nurse visit recorded successfully.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_nurse_visit_details(request):
        user_id = request.user.id
        queryset = NurseVisit.objects.filter(nurse=user_id)
        serializer = CreateNurseVisitSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def add_doctor_visit(kwargs, request):
        patient_id = kwargs['patient_id']
        request.data['patient'] = patient_id
        request.data['doctor'] = request.user.id
        operation = Operation.objects.get(patient=patient_id)
        surgeon = operation.doctor
        request.data['surgeon'] = surgeon.id
        serializer = CreateDoctorsVisitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Post Operation visit added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_doctor_visit_details(request):
        user_id = request.user.id
        queryset = DoctorsVisit.objects.filter(doctor=user_id)
        serializer = CreateDoctorsVisitSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_visit_details_by_patient(kwargs):
        patient = kwargs['patient_id']
        doctor_visit = DoctorsVisit.objects.filter(patient=patient)
        doctor_visit_serializer = CreateDoctorsVisitSerializer(doctor_visit, many=True)
        nurse_visit = NurseVisit.objects.filter(patient=patient)
        nurse_visit_serializer = CreateNurseVisitSerializer(nurse_visit, many=True)
        return Response(
            {'Nurse Visit Details': doctor_visit_serializer.data, 'Doctor Visit Details': nurse_visit_serializer.data},
            status=status.HTTP_200_OK)


class ManagePatientDetails:

    @staticmethod
    def get_operation_details(kwargs):
        operations = Operation.objects.all().order_by('-date')
        patients = operations.values('patient')
        users = User.objects.filter(id__in=patients)
        if kwargs:
            patient_id = kwargs['patient_id']
            users = users.filter(id=patient_id)
            if not users:
                return Response(
                    {'error-msg': 'Patient is not operated or'},
                    status=status.HTTP_404_NOT_FOUND)

        serializer = ViewPatientOperationSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)
