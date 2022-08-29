from rest_framework import serializers

from account.models import User, Address, Shifts
from account.serializers import AddressSerializer
from account.validations import is_contact_valid, check_birthdate
from patients.models import PatientProfile, TimeSlots, Appointment
from patients.validations import check_appointment_date, check_slot_booked, check_if_doctor, check_timeslot

BLOODGROUPS = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
               ('O-', 'O-'), ('NA', 'NA')]


class PatientRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    blood_group = serializers.ChoiceField(choices=BLOODGROUPS)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'role', 'gender',
                  'address', 'blood_group']
        read_only_fields = ['id', 'role']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        blood_group = validated_data.pop('blood_group')
        user = User.objects.create(**validated_data)
        Address.objects.create(user=user, **address_data)
        PatientProfile.objects.create(patient_id=user, blood_group=blood_group)
        return user

    def validate(self, attrs):
        birthdate = attrs.get('birthdate')
        contact = attrs.get('contact')
        is_contact_valid(contact)
        check_birthdate(birthdate)
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        patient_exists = User.objects.filter(first_name=first_name, last_name=last_name,
                                             birthdate=birthdate).exists()
        if patient_exists:
            raise serializers.ValidationError(
                "Patient already exists.")
        return attrs


class PatientUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'gender',
                  'address']
        read_only_fields = ['id']

    def validate(self, attrs):
        birthdate = attrs.get('birthdate')
        contact = attrs.get('contact')
        if contact:
            is_contact_valid(contact)
        if birthdate:
            check_birthdate(birthdate)
        return attrs

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        address_instance = Address.objects.get(user=instance.id)
        address_instance.block_no = address_data.get('block_no', address_instance.block_no)
        address_instance.building_name = address_data.get('building_name', address_instance.building_name)
        address_instance.city = address_data.get('city', address_instance.city)
        address_instance.state = address_data.get('state', address_instance.state)
        address_instance.country = address_data.get('country', address_instance.country)
        address_instance.pincode = address_data.get('pincode', address_instance.pincode)
        address_instance.save()
        return instance


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['patient_id', 'blood_group', 'disease', 'advised_procedure', 'has_allergies', 'allergies',
                  'has_medical_history', 'medical_history']
        read_only_fields = ['patient_id']


class ViewPatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    patient_profile = PatientProfileSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'role', 'gender', 'is_patient',
                  'address', 'patient_profile']
        read_only_fields = ['id', 'role']


class ViewAvailableTimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = ['id', 'start_time', 'end_time']


class ViewAvailableDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shifts
        fields = ['id', 'employee', 'shift_start', 'shift_end']


class BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'timeslot', 'doctor', 'patient']
        read_only_fields = ['id']

    def validate(self, attrs):
        date = attrs.get('date')
        timeslot = attrs.get('timeslot')
        doctor = attrs.get('doctor')
        patient = attrs.get('patient')
        # Check if doctor selected is Doctor
        check_if_doctor(doctor)
        # Check appointment date has not passed and doctor is not on leave
        check_appointment_date(date, doctor)
        # Check if timeslot is not booked by someone else
        check_slot_booked(date, timeslot, doctor)
        # Check if time of slot has not passed and if patient already has booked appointment
        check_timeslot(patient, timeslot, date, doctor)
        return attrs


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'timeslot', 'doctor', 'patient', 'status']
        read_only_fields = ['id', 'date', 'timeslot', 'doctor', 'patient']

    def validate(self, attrs):
        status = attrs.get('status')
        if status == "SCHEDULED":
            raise serializers.ValidationError(
                "Appointment status cannot be changed to scheduled. Kindly book a fresh appointment")
        return attrs

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class PatientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'contact', 'birthdate', 'gender']
        read_only_fields = ['id']


class DoctorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'contact']
        read_only_fields = ['id']


class AppointmentsSerializer(serializers.ModelSerializer):
    doctor = DoctorDetailsSerializer(many=False)
    patient = PatientDetailsSerializer(many=False)

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'timeslot', 'doctor', 'patient', 'status']
