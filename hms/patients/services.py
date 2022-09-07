import datetime
from rest_framework import status
from rest_framework.response import Response
from account.models import LeaveRequest, User
from account.queries import get_user_from_id
from patients.models import Appointment, TimeSlots, Prescription, Medication
from patients.serializers import ViewPatientSerializer, PatientRegistrationSerializer, PatientUpdateSerializer, \
    ViewAvailableTimeSlotsSerializer, BookAppointmentSerializer, UpdateAppointmentSerializer, PrescriptionSerializer, \
    UpdateMedicationSerializer, UpdateMedicinesSerializer, UpdatePatientProfileSerializer, AppointmentsSerializer


def get_on_leaves_dates(doctor):
    doctor_id = doctor.id
    print(f'DOCTOR id {doctor_id}')
    on_leave = LeaveRequest.objects.filter(employee=doctor_id, status="ACCEPTED", is_delete=False).order_by('from_date')
    print(on_leave)
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
        serializer = PatientUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageTimeSlots:
    @staticmethod
    def get_available_timeslots(request):
        appointments = Appointment.objects.filter(date=request.data['check-date'], status="SCHEDULED",
                                                  doctor=request.data['doctor'])
        booked_timeslots = []
        for appointment in appointments:
            booked_timeslots.append(appointment.timeslot.id)
        queryset = TimeSlots.objects.all().exclude(id__in=booked_timeslots)
        serializer = ViewAvailableTimeSlotsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageAppointments:
    @staticmethod
    def book_appointment(kwargs, request):
        patient_id = kwargs['pk']
        patient = get_user_from_id(patient_id)
        if patient is None:
            return Response({'error': 'Patient does not exist.'})
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
        if get_user_from_id(patient_id) is None:
            return Response({'error': 'Patient does not exist.'})
        try:
            appointments = Appointment.objects.get(id=appointment_id, status="SCHEDULED")
        except Appointment.DoesNotExist as e:
            print(e)
            return Response({'error': 'No Scheduled appointment found. Book a fresh appointment'})
        serializer = UpdateAppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def show_today_appointments():
        today = datetime.date.today()
        queryset = Appointment.objects.filter(date=today).order_by('timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def show_all_appointments():
        queryset = Appointment.objects.all().order_by('-date', 'timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def filter_doctors_appointments(doctor):
        today = datetime.date.today()
        if doctor:
            queryset = Appointment.objects.filter(doctor__first_name=doctor, date=today).order_by('timeslot')
        else:
            queryset = Appointment.objects.filter(date=today).order_by('timeslot')
        serializer = AppointmentsSerializer(queryset, many=True)
        if not serializer.data:
            return Response({"msg": "No appointments to show"}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManagePrescription:
    @staticmethod
    def generate_new_prescription(request):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def add_medicine_to_prescription(kwargs, request):
        prescription_id = kwargs['id']
        try:
            Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            return Response({'msg': 'Prescription not yet created.'}, status=status.HTTP_201_CREATED)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Medicine added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_existing_medicine(kwargs, request):
        prescription_id = kwargs['id1']
        medication_id = kwargs['id2']
        try:
            medication = Medication.objects.get(id=medication_id)
        except Medication.DoesNotExist:
            return Response({'msg': 'Medicine is not yet inserted.'}, status=status.HTTP_404_NOT_FOUND)
        request.data['prescription'] = prescription_id
        serializer = UpdateMedicinesSerializer(medication, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Prescription updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def remove_medicine_from_prescription(kwargs):
        medication_id = kwargs['id2']
        medication = Medication.objects.get(id=medication_id)
        medication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def show_prescription(kwargs):
        patient_id = kwargs['patient_id']
        queryset = Medication.objects.filter(prescription__patient__id=patient_id)
        try:
            prescription = Prescription.objects.get(patient__id=patient_id)
        except Prescription.DoesNotExist:
            return Response({"msg": "Patient's prescription is not yet created"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateMedicationSerializer(queryset, many=True)
        days = prescription.for_no_days
        return Response({"for_no_days": days, "prescription": serializer.data}, status=status.HTTP_200_OK)


class ManagePatientDetails:
    @staticmethod
    def update_medical_profile(kwargs, request):
        patient_id = kwargs['id']
        try:
            appointment = Appointment.objects.get(patient=patient_id, status="SCHEDULED")
            appointment.status = "COMPLETED"
            appointment.save()
        except Appointment.DoesNotExist as e:
            print(e)
        patient = User.objects.get(id=patient_id)
        serializer = UpdatePatientProfileSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(patient_id=patient)
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
