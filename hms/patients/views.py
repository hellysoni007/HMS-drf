import datetime

from rest_framework import generics, status
from rest_framework.response import Response

from account.models import Shifts, User
from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse
from .models import Appointment, Prescription, Medication
from .serializers import ViewAvailableDoctorsSerializer, AppointmentsSerializer, PrescriptionSerializer, \
    UpdateMedicationSerializer, UpdatePatientProfileSerializer, ShowDoctorsAppointmentsSerializer
from .services import ManagePatientRegistration, ManageTimeSlots, ManageAppointments


class ShowRegisteredPatientView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        get_patient_details = ManagePatientRegistration.view_patients(kwargs)
        return get_patient_details


class PatientRegistrationView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request):
        patient_registered = ManagePatientRegistration.register_patient(request)
        return patient_registered

    def put(self, request, **kwargs):
        update_profile = ManagePatientRegistration.update_patient_profile(kwargs, request)
        return update_profile


class ViewAvailableTimeSlots(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        timeslots = ManageTimeSlots.get_available_timeslots(request)
        return timeslots


class ViewAllDoctors(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        queryset = Shifts.objects.filter(allocated_place="OPD")
        serializer = ViewAvailableDoctorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        new_appointment = ManageAppointments.book_appointment(kwargs, request)
        return new_appointment


class UpdateAppointmentView(generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def put(self, request, **kwargs):
        update_appointment = ManageAppointments.cancel_appointment(kwargs, request)
        return update_appointment


class ShowAllAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        queryset = Appointment.objects.all().order_by('-date', 'timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowTodaysAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        queryset = Appointment.objects.filter(date=today).order_by('timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterDoctorAppointmentView(generics.RetrieveAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        doctor = self.request.query_params.get('first_name')
        today = datetime.date.today()
        if doctor:
            queryset = Appointment.objects.filter(doctor__first_name=doctor, date=today).order_by('timeslot')
        else:
            queryset = Appointment.objects.filter(date=today).order_by('timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        if not serializer.data:
            return Response({"msg": "No appointments to show"}, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePatientHealthDetails(generics.UpdateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def put(self, request, *args, **kwargs):
        patient_id = kwargs['id']
        serializer = UpdatePatientProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(patient=patient_id)
            return Response({'msg': 'Prescription created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMedicationView(generics.CreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMedicationView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        prescription_id = kwargs['id1']
        try:
            queryset = Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist as e:
            return Response({'msg': 'Prescription not yet created.'}, status=status.HTTP_201_CREATED)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Medicine added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        print(f'REQUEST {request.user}')
        prescription_id = kwargs['id1']
        medication_id = kwargs['id2']
        try:
            medication = Medication.objects.get(id=medication_id)
            # if not medication:
            #     return Response({'msg': 'Medicine is not yet inserted.'}, status=status.HTTP_404_NOT_FOUND)
        except Medication.DoesNotExist as e:
            print(e)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicationSerializer(medication, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        medication_id = kwargs['id2']
        medication = Medication.objects.get(id=medication_id)
        medication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowMedicationView(generics.ListCreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        patient_id = kwargs['patient_id']
        queryset = Medication.objects.filter(prescription__patient__id=patient_id)
        try:
            prescription = Prescription.objects.get(patient__id=patient_id)
        except Prescription.DoesNotExist as e:
            return Response({"msg": "Patient's prescription is not yet created"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateMedicationSerializer(queryset, many=True)
        days = prescription.for_no_days
        return Response({"for_no_days": days, "prescription": serializer.data}, status=status.HTTP_200_OK)


class ShowDoctorsAppointmentsView(generics.ListAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def get(self, request, *args, **kwargs):
        queryset = Appointment.objects.filter(doctor=request.user.id,status="SCHEDULED")
        serializer = ShowDoctorsAppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
