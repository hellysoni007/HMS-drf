from rest_framework import serializers

from .models import User, Address, Shifts, Rooms
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
                  'password2']
        extra_kwargs = {
            'password': {'write_only': True}

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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'birthdate', 'contact', 'email', 'joining_date', 'gender',
                  'qualifications', 'speciality']

    def validate(self, attrs):
        contact = attrs.get('contact')
        is_contact_valid(contact)
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['block_no', 'building_name', 'city', 'state', 'country', 'pincode']


class ShiftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shifts
        fields = ['allocated_shift', 'shift_start', 'shift_end', 'allocated_place']


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
