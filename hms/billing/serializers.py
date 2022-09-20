import datetime

from rest_framework import serializers

from billing.models import Bill
from .tasks import email_service


class CreateBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'patient', 'bed_charge', 'surgery_charge', 'admission_charge', 'opd_charge', 'total_charge',
                  'date',
                  'bill_details']
        read_only_fields = ['id', 'bed_charge', 'surgery_charge', 'admission_charge', 'opd_charge', 'total_charge',
                            'date',
                            'bill_details']

    def validate(self, attrs):
        patient = attrs.get('patient')
        print(patient.id)
        today = datetime.date.today()
        bill_exists = Bill.objects.filter(patient=patient, date=today)
        if bill_exists:
            raise serializers.ValidationError("Bill already generated")
        return attrs

    def create(self, validated_data):
        bill_created = Bill.objects.create(**validated_data)
        return bill_created
