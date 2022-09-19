import datetime
from rest_framework import status
from rest_framework.response import Response
from account.models import LeaveRequest, User
from account.queries import get_user_from_id
from account.services import email_service
from patients.models import Appointment, TimeSlots, Prescription, Medication
from patients.serializers import ViewPatientSerializer, PatientRegistrationSerializer, PatientUpdateSerializer, \
    ViewAvailableTimeSlotsSerializer, BookAppointmentSerializer, UpdateAppointmentSerializer, PrescriptionSerializer, \
    UpdateMedicationSerializer, UpdateMedicinesSerializer, UpdatePatientProfileSerializer, AppointmentsSerializer


def get_on_leaves_dates(doctor):
    """
    description: Logic for getting date when a particular doctor is on leave
    params: doctor
    output: leaves(list)
    """
    doctor_id = doctor.id
    on_leave = LeaveRequest.objects.filter(employee=doctor_id, status="ACCEPTED", is_delete=False).order_by('from_date')
    leaves = []
    for leave in on_leave:
        start = leave.from_date
        end = leave.to_date
        delta = datetime.timedelta(days=1)
        while start <= end:
            leaves.append(end)
            start += delta
    return leaves


class ManagePatientRegistration:
    @staticmethod
    def view_patients(kwargs):
        """
        description: Logic for displaying all patients
        params: kwargs(pk)(optional)
        output: Response(Data or error msg)
        """
        if kwargs:
            queryset = User.objects.filter(id=kwargs['pk'])
        else:
            queryset = User.objects.filter(role="Patient")
        serializer = ViewPatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def register_patient(request):
        """
        description: Logic for registering new patient
        params: Data(request)
        output: Response(Success or error msg)
        """
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role="Patient")
            return Response({'msg': 'Patient registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_patient_profile(kwargs, request):
        """
        description: Logic for updating patient profile
        params: Data(request),kwargs(pk)
        output: Response(Success or error msg)
        """
        try:
            queryset = User.objects.get(id=kwargs['pk'], role="Patient")
        except User.DoesNotExist:
            return Response({'msg': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageTimeSlots:
    @staticmethod
    def get_available_timeslots(request):
        """
        description: Logic for displaying available timeslots
        params: Data(request)
        output: Response(Data or error msg)
        """
        try:
            doctor = User.objects.get(id=request.data['doctor'])
        except User.DoesNotExist:
            return Response({'msg': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.data['doctor']:
            return Response({'msg': 'Enter Doctor to view his available timeslot'}, status=status.HTTP_400_BAD_REQUEST)
        appointments = Appointment.objects.filter(date=request.data['check-date'], status="SCHEDULED",
                                                  doctor=request.data['doctor'])
        booked_timeslots = []
        for appointment in appointments:
            booked_timeslots.append(appointment.timeslot.id)
        queryset = TimeSlots.objects.all().exclude(id__in=booked_timeslots)
        serializer = ViewAvailableTimeSlotsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def appointment_success_mail(request, patient):
    appointment_date = request.data['date']
    appointment_doctor = request.data['doctor']
    doctor = get_user_from_id(appointment_doctor)
    appointment_timeslot = request.data['timeslot']
    timeslot = TimeSlots.objects.get(id=appointment_timeslot)
    mail_to = patient.email
    mail_subject = "Appointment booked successfully"
    mail_body = f'Dear {patient.first_name},\nYour appointment for Date:{appointment_date} with Doctor:' \
                f'{doctor.first_name} in Timeslot:{timeslot.start_time} has been ' \
                f'booked successfully. '
    email_service([mail_to], mail_subject, mail_body)
    return request


def appointment_cancel_mail(appointment, patient):
    appointment_date = appointment.date
    patient = patient
    mail_to = patient.email
    mail_subject = "Your appointment has been cancelled"
    mail_body = f'Dear {patient.first_name},\n Your appointment for date {appointment_date} has been cancelled.'
    email_service([mail_to], mail_subject, mail_body)


class ManageAppointments:
    @staticmethod
    def book_appointment(kwargs, request):
        """
        description: Logic for booking appointment for a patient
        params: Data(request), kwargs(pk = patient_id)
        output: Response(Success or error msg)
        """
        patient_id = kwargs['pk']
        patient = get_user_from_id(patient_id)
        if patient is None:
            return Response({'error': 'Patient does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        # request.data._mutable = True
        request.data['patient'] = patient.id
        # request.data._mutable = False
        serializer = BookAppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            appointment_success_mail(request, patient)
            return Response({'msg': 'Appointment booked successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def cancel_appointment(kwargs, request):
        """
        description: Logic for cancelling appointment for a patient
        params: Data(request),kwargs(patient_id,appointment_id)
        output: Response(Success or error msg)
        """
        patient_id = kwargs['pk']
        appointment_id = kwargs['pk1']
        patient = get_user_from_id(patient_id)
        if get_user_from_id(patient_id) is None:
            return Response({'error': 'Patient does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            appointments = Appointment.objects.get(id=appointment_id, status="SCHEDULED")
        except Appointment.DoesNotExist as e:
            return Response({'error': 'No Scheduled appointment found. Book a fresh appointment'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateAppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            appointment = Appointment.objects.get(id=appointment_id)
            appointment_cancel_mail(appointment, patient)
            return Response({'msg': 'Appointment Cancelled successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def show_today_appointments():
        """
        description: Logic for displaying today's appointments
        params: None
        output: Response(Data)
        """
        today = datetime.date.today()
        queryset = Appointment.objects.filter(date=today).order_by('timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def show_all_appointments():
        """
        description: Logic for displaying all appointments
        params: None
        output: Response(Data)
        """
        queryset = Appointment.objects.all().order_by('-date', 'timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def filter_doctors_appointments(doctor):
        """
        description: Logic for filtering doctor's appointments
        params: doctor
        output: Response(Data or error msg)
        """
        doctor_exists = User.objects.filter(first_name=doctor, role="Doctor").exists()
        today = datetime.date.today()
        if doctor_exists:
            doctor = User.objects.get(first_name=doctor, role="Doctor")
            queryset = Appointment.objects.filter(doctor=doctor.id).filter(date=today).order_by('timeslot')
        else:
            return Response({"msg": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentsSerializer(queryset, many=True)
        if not serializer.data:
            return Response({"msg": "No appointments to show"}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagePrescription:
    @staticmethod
    def generate_new_prescription(request):
        """
        description: Logic for generating new prescription
        params: Data(request)
        output: Response(Success or error msg)
        """
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def add_medicine_to_prescription(kwargs, request):
        """
        description: Logic for adding new medicine to prescription
        params: kwargs(prescription_id),request(Data)
        output: Response(Success or error msg)
        """
        prescription_id = kwargs['id']
        try:
            Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            return Response({'msg': 'Prescription not yet created.'}, status=status.HTTP_404_NOT_FOUND)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Medicine added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_existing_medicine(kwargs, request):
        """
        description: Logic for updating existing medicine in the prescription
        params: kwargs(prescription_id,medication_id),request(Data)
        output: Response(Success or error msg)
        """
        prescription_id = kwargs['id1']
        medication_id = kwargs['id2']
        try:
            medication = Medication.objects.get(id=medication_id, prescription_id=prescription_id)
        except Medication.DoesNotExist:
            return Response({'msg': 'Invalid medication Id Or Prescription Id.'}, status=status.HTTP_404_NOT_FOUND)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicinesSerializer(medication, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def remove_medicine_from_prescription(kwargs):
        """
        description: Logic for removing medicine from prescription
        params: kwargs(prescription_id,medication_id)
        output: Response(Success or error msg)
        """
        prescription_id = kwargs['id1']
        medication_id = kwargs['id2']
        try:
            medication = Medication.objects.get(id=medication_id, prescription_id=prescription_id)
        except Medication.DoesNotExist:
            return Response({'msg': 'Invalid medicine or prescription Id'}, status=status.HTTP_404_NOT_FOUND)
        medication.delete()
        return Response({'msg': 'Medicine removed from prescription'}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def show_prescription(kwargs):
        """
        description: Logic for displaying prescription for particular patient
        params: kwargs(patient_id)
        output: Response(Data)
        """
        patient_id = kwargs['patient_id']
        try:
            User.objects.get(id=patient_id)
        except User.DoesNotExist:
            return Response({"msg": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        queryset = Medication.objects.filter(prescription__patient__id=patient_id)
        prescription = Prescription.objects.filter(patient__id=patient_id).order_by('-date')
        if not prescription:
            return Response({"msg": "Patient's prescription is not yet created"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateMedicationSerializer(queryset, many=True)
        days = prescription[0].for_no_days
        return Response({"for_no_days": days, "prescription": serializer.data}, status=status.HTTP_200_OK)


class ManagePatientDetails:
    @staticmethod
    def update_medical_profile(kwargs, request):
        """
        description: Logic for updating patient profile
        params: request(Data),kwargs(patient_id)
        output: Response(Success or error msg)
        """
        patient_id = kwargs['id']
        try:
            appointment = Appointment.objects.get(patient=patient_id, status="SCHEDULED")
            appointment.status = "COMPLETED"
            appointment.save()
        except Appointment.DoesNotExist as e:
            print(e)
        try:
            patient = User.objects.get(id=patient_id)
        except User.DoesNotExist:
            return Response({'msg': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdatePatientProfileSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(patient_id=patient)
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
