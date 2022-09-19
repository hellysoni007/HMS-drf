import datetime

from account import serializers
from account.models import Shifts, Substitution, User
from operation.models import Bed, Admission
from patients.services import get_on_leaves_dates


def bed_exists(name, room):
    """
    Returns bed object if bed exists
    """
    try:
        bed = Bed.objects.get(name=name, room=room)
        return bed
    except Bed.DoesNotExist:
        return False


def check_appointment_date(date, doctor):
    """
    check if appointment for the selected doctor is valid or not
    """
    if date < datetime.date.today():
        raise serializers.ValidationError(
            "Date entered is not valid.")
    try:
        substitute = Substitution.objects.get(for_date=date, substitute=doctor)
        if substitute:
            return True
    except Substitution.DoesNotExist:
        leave_dates = get_on_leaves_dates(doctor)
        if date in leave_dates:
            shift = Shifts.objects.get(employee=doctor)
            shift_id = shift.id
            substitute_object = Substitution.objects.get(shift=shift_id)
            substitute_id = substitute_object.substitute.id
            substitute_doctor = User.objects.get(id=substitute_id)
            raise serializers.ValidationError(
                f"Surgeon selected is unavailable for the day.Available doctor is {substitute_doctor.first_name}")
        else:
            return True




