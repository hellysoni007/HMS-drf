import datetime

from rest_framework import serializers

from billing.models import Bill
from account.services import email_service


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
        patient = validated_data.get('patient')
        mail_body = "Bill details: " + '\n' + f'Bill Date: {bill_created.date}\nBill Id : {bill_created.id}\nBed ' \
                                              f'charge : ' \
                                              f'{bill_created.bed_charge}\nSurgery Charge : ' \
                                              f'{bill_created.surgery_charge}\nAdmission ' \
                                              f'Charge : {bill_created.admission_charge}\nOPD Charge : ' \
                                              f'{bill_created.opd_charge}\nTotal : {bill_created.total_charge}'
        email_service([patient], "Your today's bill", mail_body)
        return bill_created
