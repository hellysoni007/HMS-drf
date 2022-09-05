import datetime

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse
from operation.models import Bed, Operation
from operation.serializers import CreateBedSerializer, DisplayBedSerializer, UpdateBedSerializer, \
    UpdateBedAvailabilitySerializer, ScheduleOperationSerializer, ShowAllOperationsSerializer, \
    UpdateOperationsSerializer
from patients.models import PatientProfile


# Create your views here.

# View available surgeons for operation
# View available timeslots for operation

# View all bed details(Who on which bed, is_available)
# add admission details, update admission details (Admission time,Discharge time)
# View admission details
# add operation details
# View all scheduled operation for Receptionist(order by date)
# View all scheduled operation for Receptionist(filter by today)
# View all scheduled operation for Receptionist(filter by doctors,order by date)
# View all operations for Receptionist(order by date)
# View all operations for Receptionist(filter by today)
# View all operations for Receptionist(filter by doctors,order by date)
# View scheduled operation for logged in surgeon(filter by date,status)
# update bed occupation status(Admission time,Discharge time)
# View patients as per bed,rooms
# Update operation status and add instructions


# Add post op check details for nurse
# Add post op check details for doctor
# View post op check details for nurse,doctor
# Update post op check specific details for nurse , doctor

class CreateUpdateBedView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateBedSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Bed added successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
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


class UpdateBedAvailabilityView(generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def put(self, request, *args, **kwargs):
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


class DeleteBedView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
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


class DisplayBedsView(generics.ListAPIView):
    permission_classes = [IsAdminUser | IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        if kwargs:
            bed_id = kwargs['id']
            queryset = Bed.objects.filter(id=bed_id).exclude(is_delete=True)
            if not queryset:
                return Response({'msg': 'Bed not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Bed.objects.all().exclude(is_delete=True)
        serializer = DisplayBedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View available beds
class DisplayAvailableBedsView(generics.ListAPIView):
    permission_classes = [IsAdminUser | IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        bed_id = self.request.query_params['bed_id']
        if bed_id:
            queryset = Bed.objects.filter(id=bed_id, is_available=True).exclude(is_delete=True)
            if not queryset:
                return Response({'msg': 'Bed not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Bed.objects.filter(is_available=True, is_delete=False)
        serializer = DisplayBedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Operation views

# Schedule Operation
class ScheduleOperationView(generics.CreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        patient_id = kwargs['patient_id']
        try:
            patient_profile = PatientProfile.objects.get(patient_id=patient_id)
            if patient_profile.advise != 'Operation':
                return Response({'error-msg': 'Patient is not advised for operation.'}, status=status.HTTP_201_CREATED)
        except PatientProfile.DoesNotExist:
            return Response({'error-msg': 'Invalid patient Id.'}, status=status.HTTP_201_CREATED)

        request.data['patient'] = patient_id
        print(request.data)
        serializer = ScheduleOperationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status='SCHEDULED')
            return Response({'msg': 'Operation scheduled successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Show all operations and view operation details
class ShowOperationsView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        op_id = self.request.query_params['op_id']
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            queryset = Operation.objects.all().order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowTodayDoctorOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs['doctor_id']
        op_id = self.request.query_params['op_id']
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            today = datetime.date.today()
            queryset = Operation.objects.filter(doctor=doctor_id, date=today)
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowDoctorOperationView(generics.ListAPIView):
    permission_classes = [IsSurgeon]

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs['doctor_id']
        op_id = self.request.query_params['op_id']
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            queryset = Operation.objects.filter(doctor=doctor_id).order_by('date')
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowTodayOperationView(generics.ListAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        op_id = self.request.query_params['op_id']
        if op_id:
            queryset = Operation.objects.filter(id=op_id).order_by('date')
        else:
            today = datetime.date.today()
            queryset = Operation.objects.filter(date=today)
        serializer = ShowAllOperationsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateOperationDetailView(generics.UpdateAPIView):
    permission_classes = [IsSurgeon]

    def put(self, request, *args, **kwargs):
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


class CreatePatientAdmissionDetailsView(generics.CreateAPIView, generics.UpdateAPIView):
    pass


class ListUpdatePatientAdmissionDetailsView(generics.UpdateAPIView, generics.ListAPIView):
    pass


class DisplayCurrentlyAdmittedPatientsView(generics.ListAPIView):
    pass


class DisplayAllAdmittedPatientsView(generics.ListAPIView):
    pass
