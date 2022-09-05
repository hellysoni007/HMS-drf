from rest_framework import serializers

from account.models import Rooms
from account.queries import get_user_from_id
from operation.models import Bed, Operation
from operation.validations import bed_exists, check_appointment_date
from patients.serializers import ViewPatientSerializer


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
