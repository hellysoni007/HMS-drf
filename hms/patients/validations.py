import datetime

from rest_framework import serializers

from account.models import Substitution, Shifts, User
from patients.models import Appointment, TimeSlots


def check_if_doctor(doctor):
    """
    Check if employee is a doctor or surgeon
    """
    if doctor.role == "Doctor" or doctor.role == "Surgeon":
        return doctor
    else:
        raise serializers.ValidationError(
            "Please enter a doctor.")


def check_appointment_date(date, doctor):
    """
    check appointment date is not in the past and doctor selected is not on leave
    """
    from patients.services import get_on_leaves_dates
    today = datetime.date.today()

    if date < today:
        raise serializers.ValidationError(
            "Date entered is not valid.")
    leave_dates = get_on_leaves_dates(doctor)
    if date in leave_dates:
        shift = Shifts.objects.get(employee=doctor)
        shift_id = shift.id
        substitute_object = Substitution.objects.get(shift=shift_id)
        substitute_id = substitute_object.substitute.id
        substitute_doctor = User.objects.get(id=substitute_id)
        raise serializers.ValidationError(
            f"Doctor selected is unavailable for the day.Available doctor is {substitute_doctor.first_name}")


def check_slot_booked(date, timeslot, doctor):
    """
    check if selected slot is already booked
    """
    slot_already_booked = Appointment.objects.filter(date=date, timeslot=timeslot, doctor=doctor,
                                                     status='SCHEDULED').exists()
    if slot_already_booked:
        raise serializers.ValidationError(
            "This time slot is already booked.Book another time slot")


def check_timeslot(patient, timeslot, date, doctor):
    """
    check if timeslot has not passed and appointment for patient is not already booked
    """
    timeslot_object = TimeSlots.objects.get(id=timeslot.id)
    now_time = datetime.datetime.now()
    now_time = now_time.time()
    if timeslot_object.start_time < now_time and date < datetime.date.today():
        raise serializers.ValidationError(
            "TimeSlot cannot be booked as slot time already passed.")

    appointment_already_booked = Appointment.objects.filter(patient=patient, status='SCHEDULED')
    appointment_already_completed = Appointment.objects.filter(date=date, timeslot=timeslot, doctor=doctor,
                                                               status='COMPLETED')
    if appointment_already_booked:
        raise serializers.ValidationError(
            "Patient's appointment is already booked.")

    if appointment_already_completed:
        raise serializers.ValidationError(
            "TimeSlot is already booked.")
