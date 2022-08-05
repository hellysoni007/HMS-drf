from rest_framework import serializers

from .models import User
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
        fields = ['email', 'first_name', 'last_name', 'contact', 'birthdate', 'gender', 'role', 'password', 'password2']
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
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'birthdate', 'contact', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'email']

# class PatientSerializer(serializers.ModelSerializer):
#     queryset = User.objects.filter(role="Patient")
#     serializer = UserSerializer(queryset,many=True)
#     serializer.data
