import datetime
from datetime import date
import pytest

from account.models import User
from billing.models import Bill


@pytest.fixture
@pytest.mark.django_db
def create_user_fixture():
    user = User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user',
                                    contact='7894562314', birthdate=date(2016, 9, 1), gender='FEMALE',
                                    role='Patient', password='Admin@123', password2='Admin@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_bill_fixture(create_user_fixture):
    bill = Bill.objects.create(patient=create_user_fixture, bed_charge=500, surgery_charge=6000, admission_charge=5000,
                               opd_charge=0, total_charge=11500, date=datetime.date.today(),
                               bill_details={'op_id': 5})
    return bill


class TestBillModel:
    @pytest.mark.django_db
    def test_bill_model(self, create_user_fixture):
        Bill.objects.create(patient=create_user_fixture, bed_charge=500, surgery_charge=6000,
                            admission_charge=5000,
                            opd_charge=0, total_charge=11500, date=datetime.date.today(),
                            bill_details={'op_id': 5})
        assert Bill.objects.filter(patient=create_user_fixture, date=datetime.date.today()).exists()

    @pytest.mark.django_db
    def test_patient_field(self, create_user_fixture, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.patient == create_user_fixture

    @pytest.mark.django_db
    def test_bed_charge_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.bed_charge == 500

    @pytest.mark.django_db
    def test_surgery_charge_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.surgery_charge == 6000

    @pytest.mark.django_db
    def test_admission_charge_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.admission_charge == 5000

    @pytest.mark.django_db
    def test_opd_charge_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.opd_charge == 0

    @pytest.mark.django_db
    def test_total_charge_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.total_charge == 11500

    @pytest.mark.django_db
    def test_date_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.date == datetime.date.today()

    @pytest.mark.django_db
    def test_bill_details_field(self, create_bill_fixture):
        bill = create_bill_fixture
        assert bill.bill_details == {'op_id': 5}
