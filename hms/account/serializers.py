import datetime

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import User, Address, Shifts, Rooms, LeaveRequest
from .queries import get_user_from_mail, get_user_from_id
from .validations import is_contact_valid, check_password_match


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
        check_password_match(password, password2)
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
        print(f'employee_id{employee_id}')
        # print(get_user_from_id(employee_id))

        employee_object = get_user_from_mail(employee_id)
        print(employee_object.role)
        rooms = Rooms.objects.filter()
        room_list = []
        for room in rooms:
            room_list.append(room.name)
        print(rooms)
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
        fields = ['id', 'employee', 'applied_on', 'from_date', 'to_date', 'reason', 'status']
        read_only_fields = ['id', 'employee', 'applied_on', 'from_date', 'to_date', 'reason']


class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'applied_on', 'from_date', 'to_date', 'reason', 'status']
        read_only_fields = ['id', 'applied_on', 'status']

    def validate(self, attrs):
        from_date = attrs.get('from_date')
        if from_date < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
        else:
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


# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'role', ]

class PatientSerializer(serializers.ModelSerializer):
    queryset = User.objects.filter(role="Patient")

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'role', ]
        read_only_fields = ['id', 'role']
