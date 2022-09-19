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
        """
        description: Show registered patients
        params: patient_id(optional)
        output: patients
        """
        get_patient_details = ManagePatientRegistration.view_patients(kwargs)
        return get_patient_details


class PatientRegistrationView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        description: Register new patients
        params: None
        output: success or failure msg
        """
        patient_registered = ManagePatientRegistration.register_patient(request)
        return patient_registered

    def put(self, request, **kwargs):
        """
        description: Update patient details
        params: patient_id
        output: success or failure url
        """
        update_profile = ManagePatientRegistration.update_patient_profile(kwargs, request)
        return update_profile


class ViewAvailableTimeSlots(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Get available timeslots
        params: None
        output: timeslots
        """
        timeslots = ManageTimeSlots.get_available_timeslots(request)
        return timeslots


class ViewAllDoctors(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Get all doctors
        params: None
        output: doctors
        """
        queryset = Shifts.objects.filter(allocated_place="OPD")
        serializer = ViewAvailableDoctorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def post(self, request, *args, **kwargs):
        """
        description: Book appointment for registered patient
        params: patient_id
        output: success or failure msg
        """
        new_appointment = ManageAppointments.book_appointment(kwargs, request)
        return new_appointment


class UpdateAppointmentView(generics.UpdateAPIView):
    permission_classes = [IsReceptionist]

    def put(self, request, **kwargs):
        """
        description: Cancel appointment
        params: patient_id,appointment_id
        output: success or failure msg
        """
        update_appointment = ManageAppointments.cancel_appointment(kwargs, request)
        return update_appointment


class ShowAllAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Show all appointments
        params: None
        output: appointments
        """
        appointments = ManageAppointments.show_all_appointments()
        return appointments


class ShowTodaysAppointmentView(generics.ListCreateAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Show todays appointmenta
        params: None
        output: appointments
        """
        appointments = ManageAppointments.show_today_appointments()
        return appointments


class FilterDoctorAppointmentView(generics.RetrieveAPIView):
    permission_classes = [IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Filter appointments by doctor
        params: first_name(doctor's)
        output: appointments
        """
        doctor = request.query_params.get('first_name')
        print(f'DOCTOR ------- {doctor}')
        appointments = ManageAppointments.filter_doctors_appointments(doctor)
        return appointments


class UpdatePatientHealthDetails(generics.UpdateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def put(self, request, *args, **kwargs):
        """
        description: Update patient health details
        params: patient_id
        output: success or failure msg
        """
        update_details = ManagePatientDetails.update_medical_profile(kwargs, request)
        return update_details


class CreateMedicationView(generics.CreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        """
        description: Generate prescription for patients
        params: None
        output: success of failure msg
        """
        new_prescription = ManagePrescription.generate_new_prescription(request)
        return new_prescription


class UpdateMedicationView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def post(self, request, *args, **kwargs):
        """
        description: add medicine to prescription
        params: prescription_id
        output: success or failure msg
        """
        add_medicine = ManagePrescription.add_medicine_to_prescription(kwargs, request)
        return add_medicine

    def put(self, request, *args, **kwargs):
        """
        description: Update medicine details in prescription
        params: prescription_id,medication_id
        output: success or failure msg
        """
        update_medicine = ManagePrescription.update_existing_medicine(kwargs, request)
        return update_medicine

    def delete(self, *args, **kwargs):
        """
        description: Remove medicine from prescription
        params: prescription_id,medication_id
        output: success or failure msg
        """
        remove_medicine = ManagePrescription.remove_medicine_from_prescription(kwargs)
        return remove_medicine


class ShowMedicationView(generics.ListCreateAPIView):
    permission_classes = [IsDoctor | IsSurgeon | IsNurse | IsReceptionist]

    def get(self, request, *args, **kwargs):
        """
        description: Show prescription details
        params: patient_id
        output: prescription
        """
        view_prescription = ManagePrescription.show_prescription(kwargs)
        return view_prescription


class ShowDoctorsAppointmentsView(generics.ListAPIView):
    permission_classes = [IsDoctor | IsSurgeon]

    def get(self, request, *args, **kwargs):
        """
                description: Show log in doctors appointments
                params: None
                output: appointments
                """
        queryset = Appointment.objects.filter(doctor=request.user.id, status="SCHEDULED").order_by('timeslot')
        serializer = ShowDoctorsAppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
