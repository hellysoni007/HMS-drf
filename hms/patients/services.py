import datetime

from rest_framework import status
from rest_framework.response import Response

from account.models import LeaveRequest, User
from patients.models import Appointment, TimeSlots
from patients.serializers import ViewPatientSerializer, PatientRegistrationSerializer, PatientUpdateSerializer, \
    ViewAvailableTimeSlotsSerializer, BookAppointmentSerializer, UpdateAppointmentSerializer


def get_on_leaves_dates(doctor):
    on_leave = LeaveRequest.objects.filter(employee=doctor, status="ACCEPTED").order_by('from_date')
    leaves = []
    for leave in on_leave:
        start = leave.from_date
        end = leave.to_date
        delta = datetime.timedelta(days=1)
        while start <= end:
            print(end.strftime("%Y-%m-%d"))
            leaves.append(end)
            start += delta
    return leaves


class ManagePatientRegistration:
    @staticmethod
    def view_patients(kwargs):
        if kwargs:
            queryset = User.objects.filter(id=kwargs['pk'])
        else:
            queryset = User.objects.filter(role="Patient")
        serializer = ViewPatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def register_patient(request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role="Patient")
            result = Response({'msg': 'Patient registered successfully.'}, status=status.HTTP_201_CREATED)
            return result
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_patient_profile(kwargs, request):
        queryset = User.objects.get(id=kwargs['pk'])
        print(queryset)
        serializer = PatientUpdateSerializer(queryset, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageTimeSlots:
    @staticmethod
    def get_available_timeslots(request):
        appointments = Appointment.objects.filter(date=request.data['check-date'], status="SCHEDULED")
        booked_timeslots = []
        for appointment in appointments:
            booked_timeslots.append(appointment.timeslot.id)
        queryset = TimeSlots.objects.all().exclude(id__in=booked_timeslots)
        serializer = ViewAvailableTimeSlotsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageAppointments:
    @staticmethod
    def book_appointment(kwargs, request):
        patient = User.objects.get(id=kwargs['pk'])
        request.data['patient'] = patient.id
        serializer = BookAppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Appointment booked successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def cancel_appointment(kwargs, request):
        patient_id = kwargs['pk']
        appointment_id = kwargs['pk1']
        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist as e:
            return Response({'error': 'Patient does not exist.'})
        try:
            appointments = Appointment.objects.get(id=appointment_id, status="SCHEDULED")
        except Appointment.DoesNotExist as e:
            return Response({'error': 'No Scheduled appointment found. Book a fresh appointment'})
        serializer = UpdateAppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
