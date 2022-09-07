import datetime

from rest_framework import serializers

from account.models import Rooms, User
from account.queries import get_user_from_id
from account.serializers import AddressSerializer
from operation.models import Bed, Operation, Admission, NurseVisit, DoctorsVisit
from operation.validations import bed_exists, check_appointment_date
from patients.models import PatientProfile
from patients.serializers import ViewPatientSerializer, PatientProfileSerializer


class CreateBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['name', 'room', 'is_available', 'charges_per_day']

    def validate(self, attrs):
        name = attrs.get('name')
        room = attrs.get('room')
        if bed_exists(name, room):
            raise serializers.ValidationError(
                "Bed with this name already exists.")
        return attrs


class UpdateBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['name', 'room', 'is_available', 'charges_per_day']

    def validate(self, attrs):
        if attrs.get('name') and attrs.get('room'):
            name = attrs.get('name')
            room = attrs.get('room')
            if bed_exists(name, room):
                raise serializers.ValidationError(
                    "Bed with this name already exists.")
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.room = validated_data.get('room', instance.room)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.charges_per_day = validated_data.get('charges_per_day', instance.charges_per_day)
        instance.save()
        return instance


class UpdateBedAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['is_available']

    def validate(self, attrs):
        if not attrs.get('is_available'):
            raise serializers.ValidationError(
                "Enter status to update.")
        return attrs

    def update(self, instance, validated_data):
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['name', 'type', 'assigned_nurses']


class DisplayBedSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)

    class Meta:
        model = Bed
        fields = ['name', 'room', 'is_available', 'charges_per_day']


class ScheduleOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['doctor', 'patient', 'operation-name', 'date', 'timeslot', 'status']
        read_only_fields = ['status']

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        patient = attrs.get('patient')

        # Check if doctor is Surgeon
        doctor_obj = get_user_from_id(doctor.id)
        if doctor_obj.role != "Surgeon":
            raise serializers.ValidationError(
                "Enter valid surgeon Id.")

        # Check if patient operation is already scheduled
        operation = Operation.objects.filter(patient=patient, status='SCHEDULED')
        if operation:
            raise serializers.ValidationError(
                "Operation is already scheduled for patient.")

        date = attrs.get('date')
        if date < datetime.date.today():
            raise serializers.ValidationError(
                "Invalid date.")

        if not check_appointment_date(date, doctor):
            print("Operation not scheduled")
            raise serializers.ValidationError(
                "Doctor unavailable.")

        timeslot = attrs.get('timeslot')

        # check timeslot for operation
        if timeslot.id not in range(31, 39, 1):
            print(timeslot.id)
            raise serializers.ValidationError(
                "Enter valid timeslot for operation.")

        # check if timeslot and doctor has already been booked for operation
        operation = Operation.objects.filter(doctor=doctor, date=date, timeslot=timeslot)
        if operation:
            raise serializers.ValidationError(
                "Operation is already scheduled for this time.")
        return attrs


class ShowAllOperationsSerializer(serializers.ModelSerializer):
    patient = ViewPatientSerializer(many=False, read_only=True)

    class Meta:
        model = Operation
        fields = ['doctor', 'patient', 'operation-name', 'date', 'timeslot', 'status']


class UpdateOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['status', 'instructions']

    def validate(self, attrs):
        status = attrs.get('status')
        print(status)
        if status != 'COMPLETED':
            raise serializers.ValidationError("Invalid operation status")
        return attrs

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.save()
        return instance


class CreatePatientAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ['patient', 'bed']

    # While creation update bed model

    def validate(self, attrs):

        # check if patient is to be operated
        patient = attrs.get('patient')
        print(patient)
        if not patient:
            raise serializers.ValidationError("Invalid patient ID")

        patient_profile = PatientProfile.objects.get(patient_id=patient)
        if patient_profile.advise != "Operation":
            raise serializers.ValidationError("Patient does not need to be admitted")

        # Check if bed available
        bed = attrs.get('bed')
        print(bed.is_available)
        if not bed.is_available:
            raise serializers.ValidationError("Selected Bed not available.")
        return attrs

    def create(self, validated_data):
        # While creation update bed model
        bed = validated_data.get('bed')
        patient = validated_data.get('patient')
        print(bed)
        # bed_obj = Bed.objects.get(id=bed)
        bed.is_available = False
        bed.save()

        operation_obj = Operation.objects.get(patient=patient)
        admission_date = operation_obj.date - datetime.timedelta(days=1)
        print(admission_date)
        # raise serializers.ValidationError("Check details")
        # Admission date will be one day prior to operation date
        created_obj = Admission.objects.create(admission_date=admission_date, **validated_data)
        return created_obj


class UpdatePatientAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ['patient', 'discharge_date', 'admission_date']
        read_only_fields = ['patient', 'admission_date']

    def validate(self, attrs):
        today = datetime.datetime.today()
        discharge_date = attrs.get('discharge_date')
        if discharge_date.timestamp() <= today.timestamp():
            raise serializers.ValidationError("Invalid date.")
        return attrs

    def update(self, instance, validated_data):
        pass


class DisplayPatientAdmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ['id', 'patient', 'bed', 'admission_date', 'discharge_date']


class DisplayPatientOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['patient', 'operation-name', 'date', 'timeslot', 'status', 'instructions']


class ShowNurseVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseVisit
        fields = ['patient', 'nurse', 'surgeon', 'medication_time', 'is_medication_provided']


class CreateNurseVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseVisit
        fields = ['patient', 'nurse', 'surgeon', 'is_medication_provided']


class ShowDoctorsVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsVisit
        fields = ['patient', 'doctor', 'surgeon', 'is_normal', 'is_visit_done']


class CreateDoctorsVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsVisit
        fields = ['patient', 'doctor', 'surgeon', 'is_normal']

    def validate(self, attrs):
        # check doctor not on leave

        return attrs


class ViewPatientOperationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    patient_profile = PatientProfileSerializer(many=True)
    operated_patient = DisplayPatientOperationSerializer(many=True)
    patient_to_visit = ShowDoctorsVisitSerializer(many=True)
    to_visit = ShowNurseVisitSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'birthdate', 'role', 'gender', 'is_patient',
                  'address', 'patient_profile', 'operated_patient', 'patient_to_visit', 'to_visit']
        read_only_fields = ['id', 'role']
