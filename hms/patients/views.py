from rest_framework import generics, status
from rest_framework.response import Response

from account.models import Shifts
from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse
from .models import Appointment
from .serializers import ViewAvailableDoctorsSerializer, ShowDoctorsAppointmentsSerializer
from .services import ManagePatientRegistration, ManageTimeSlots, ManageAppointments, ManagePrescription, \
    ManagePatientDetails


class ShowRegisteredPatientView(generics.ListAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        get_patient_details = ManagePatientRegistration.view_patients(kwargs)
        return get_patient_details


class PatientRegistrationView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
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
        appointments = ManageAppointments.show_all_appointments()
        return appointments


class ShowTodaysAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        appointments = ManageAppointments.show_today_appointments()
        return appointments


class FilterDoctorAppointmentView(generics.RetrieveAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        doctor = self.request.query_params.get('first_name')
        appointments = ManageAppointments.filter_doctors_appointments(doctor)
        return appointments


class UpdatePatientHealthDetails(generics.UpdateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def put(self, request, *args, **kwargs):
        update_details = ManagePatientDetails.update_medical_profile(kwargs, request)
        return update_details


class CreateMedicationView(generics.CreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        new_prescription = ManagePrescription.generate_new_prescription(request)
        return new_prescription


class UpdateMedicationView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        add_medicine = ManagePrescription.add_medicine_to_prescription(kwargs, request)
        return add_medicine

    def put(self, request, *args, **kwargs):
        update_medicine = ManagePrescription.update_existing_medicine(kwargs, request)
        return update_medicine

    def delete(self, *args, **kwargs):
        remove_medicine = ManagePrescription.remove_medicine_from_prescription(kwargs)
        return remove_medicine


class ShowMedicationView(generics.ListCreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        view_prescription = ManagePrescription.show_prescription(kwargs)
        return view_prescription


class ShowDoctorsAppointmentsView(generics.ListAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def get(self, request, *args, **kwargs):
        queryset = Appointment.objects.filter(doctor=request.user.id, status="SCHEDULED").order_by('timeslot')
        serializer = ShowDoctorsAppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
