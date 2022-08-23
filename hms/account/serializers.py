import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Address, Shifts, Rooms, LeaveRequest, Substitution
from .queries import get_user_from_mail, get_user_from_id

from .validations import is_contact_valid, check_password_match, check_birthdate


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """We need password2 field in our registration request"""

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'contact', 'birthdate', 'gender', 'role', 'password',
                  'password2', 'joining_date']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # Validating password and confirm password while Registration
    def validate(self, attrs):
        contact = attrs.get('contact')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        birthdate = attrs.get('birthdate')
        check_password_match(password, password2)
        check_birthdate(birthdate)
        is_contact_valid(contact)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['block_no', 'building_name', 'city', 'state', 'country', 'pincode']


class ShiftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shifts
        fields = ['employee', 'allocated_shift', 'shift_start', 'shift_end', 'allocated_place']

    def validate(self, attrs):
        allocated_place = attrs.get('allocated_place')
        employee_id = attrs.get('employee')

        employee_object = get_user_from_mail(employee_id)
        if not employee_object:
            raise serializers.ValidationError(
                "Employee does not exist.")
        rooms = Rooms.objects.filter()
        room_list = []
        for room in rooms:
            room_list.append(room.name)
        if (employee_object.role == 'Nurse') and (allocated_place in room_list):
            return attrs
        elif employee_object.role == 'Receptionist' and allocated_place == 'Reception':
            return attrs
        elif employee_object.role == 'Doctor' and allocated_place == 'OPD':
            return attrs
        elif employee_object.role == 'Surgeon' and allocated_place in ['OT', 'OPD']:
            return attrs
        else:
            raise serializers.ValidationError(
                "Allocation place does not match the role.")


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'applied_on', 'from_date', 'to_date', 'reason', 'status', 'has_substitute']
        read_only_fields = ['id', 'employee', 'applied_on', 'from_date', 'to_date', 'reason']


class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'applied_on', 'from_date', 'to_date', 'reason', 'status']
        read_only_fields = ['id', 'applied_on', 'status']

    def validate(self, attrs):
        """
        :param attrs:
        :return:
        """
        from_date = attrs.get('from_date')
        to_date = attrs.get('to_date')
        if from_date and to_date:
            if from_date < datetime.date.today():
                raise ValidationError("The date cannot be in the past!")
            if from_date > to_date:
                raise ValidationError("The leaves starting date can not be a dater after leaves ending date.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    address = AddressSerializer(many=True)
    shift = ShiftsSerializer(many=True)
    leaves = LeaveRequestSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'birthdate', 'contact', 'email', 'joining_date', 'gender',
                  'qualifications', 'speciality', 'address', 'shift', 'leaves']
        read_only_fields = ['id']

    def validate(self, attrs):
        contact = attrs.get('contact')
        is_contact_valid(contact)
        return attrs


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['name', 'type', 'no_of_beds', 'assigned_nurses']


def get_dates(start, end):
    step = datetime.timedelta(days=1)
    date_list = []
    while start <= end:
        if start > datetime.date.today():
            date_list.append(start)
        start += step
    return date_list


def substitute_on_leave(employee_id, date_check):
    substitute_leaves = LeaveRequest.objects.filter(employee=employee_id)
    dates = []
    for leave in substitute_leaves:
        start = leave.from_date
        end = leave.to_date
        dates = dates + get_dates(start, end)
    if date_check in dates:
        return True
    else:
        return False


class GetSubstitutionSerializer(serializers.ModelSerializer):
    substitute = serializers.SerializerMethodField()

    def get_substitute(self, obj):
        return obj.substitute.email

    class Meta:
        model = Substitution
        fields = ['id', 'shift', 'for_date', 'substitute']
        read_only_fields = ['id']


class SubstitutionSerializer(serializers.ModelSerializer):
    substitute = serializers.ChoiceField(
        choices=User.objects.all())

    class Meta:
        model = Substitution
        fields = ['id', 'shift', 'for_date', 'substitute']
        read_only_fields = ['id']

    def validate(self, attrs):
        shift_id_get = attrs.get('shift')
        for_date = attrs.get('for_date')
        print(for_date)
        substitute_emp = attrs.get('substitute')
        if Substitution.objects.filter(shift=shift_id_get, for_date=for_date).exists():
            raise serializers.ValidationError(
                "Substitute is already assigned.")
        print(substitute_emp)
        if substitute_on_leave(substitute_emp.id, for_date):
            print("True")
            raise serializers.ValidationError(
                "Substitute is also on leave for the day.Enter another substitute.")
        if shift_id_get.employee.role != substitute_emp.role:
            raise serializers.ValidationError(
                "Sorry cannot substitute employee with a different role.")
        return attrs
