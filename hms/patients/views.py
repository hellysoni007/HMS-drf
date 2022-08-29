import datetime

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from account.models import Shifts, User
from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse
from .models import Appointment
from .serializers import ViewAvailableDoctorsSerializer, AppointmentsSerializer
from .services import ManagePatientRegistration, ManageTimeSlots, ManageAppointments


class PatientRegistrationView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist, IsDoctor, IsSurgeon, IsNurse])
    def get(self, request, *args, **kwargs):
        get_patient_details = ManagePatientRegistration.view_patients(kwargs)
        return get_patient_details

    @permission_classes([IsReceptionist])
    def post(self, request):
        patient_registered = ManagePatientRegistration.register_patient(request)
        return patient_registered

    @permission_classes([IsReceptionist])
    def put(self, request, **kwargs):
        update_profile = ManagePatientRegistration.update_patient_profile(kwargs, request)
        return update_profile


class ViewAvailableTimeSlots(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def get(self, request):
        timeslots = ManageTimeSlots.get_available_timeslots(request)
        return timeslots


class ViewAllDoctors(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def get(self, request):
        queryset = Shifts.objects.filter(allocated_place="OPD")
        serializer = ViewAvailableDoctorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Takes date
# class ViewDoctorsAvailability()


class BookAppointmentView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def post(self, request, *args, **kwargs):
        new_appointment = ManageAppointments.book_appointment(kwargs, request)
        return new_appointment


class UpdateAppointmentView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def put(self, request, **kwargs):
        update_appointment = ManageAppointments.cancel_appointment(kwargs, request)
        return update_appointment


class ShowAllAppointmentView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def get(self, request):
        queryset = Appointment.objects.all().order_by('date')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowTodaysAppointmentView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist])
    def get(self, request):
        today = datetime.date.today()
        queryset = Appointment.objects.filter(date=today)
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterDoctorsAppointmentView(generics.RetrieveAPIView):
    @permission_classes([IsReceptionist])
    def get(self, request):
        if request.data:
            doctor_name = request.data['doctor']
            get_doctor = User.objects.get(first_name=doctor_name)
            queryset = Appointment.objects.filter(doctor=get_doctor.id)
        else:
            queryset = Appointment.objects.all()
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
