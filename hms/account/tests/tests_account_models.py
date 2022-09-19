import datetime
from datetime import date
import pytest

from account.models import User, Shifts, Substitution, Rooms, LeaveRequest


@pytest.fixture
@pytest.mark.django_db
def create_user_fixture():
    user = User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user',
                                    contact='7894562314', birthdate=date(2016, 9, 1), gender='FEMALE',
                                    role='Receptionist', password='Admin@123', password2='Admin@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse_fixture():
    user = User.objects.create_user(email='testnurse1@gmail.com', first_name='nurse', last_name='user',
                                    contact='7894562314', birthdate=date(2016, 9, 1), gender='FEMALE',
                                    role='Nurse', password='Admin@123', password2='Admin@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_nurse_fixture2():
    user = User.objects.create_user(email='testnurse2@gmail.com', first_name='nurse1', last_name='user',
                                    contact='7894562314', birthdate=date(2016, 9, 1), gender='FEMALE',
                                    role='Nurse', password='Admin@123', password2='Admin@123')
    return user


@pytest.fixture
@pytest.mark.django_db
def create_substitution_fixture(create_nurse_fixture, create_nurse_fixture2):
    shift = Shifts.objects.create(employee=create_nurse_fixture, allocated_shift=1, shift_start=datetime.time(10, 0, 0),
                                  shift_end=datetime.time(10, 30, 0), allocated_place="A")
    substitution = Substitution.objects.create(shift=shift, for_date=datetime.date(2022, 9, 17),
                                               substitute=create_nurse_fixture2)
    return shift, substitution


@pytest.fixture
@pytest.mark.django_db
def create_shift_fixture(create_user_fixture):
    employee = create_user_fixture
    shift = Shifts.objects.create(employee=employee, allocated_shift=1, shift_start=datetime.time(10, 0, 0),
                                  shift_end=datetime.time(10, 30, 0), allocated_place="OT")
    return shift


@pytest.fixture
@pytest.mark.django_db
def create_room_fixture():
    room = Rooms.objects.create(name="A", type="General", no_of_beds=5)
    return room


@pytest.fixture
@pytest.mark.django_db
def create_leave_request_fixture(create_user_fixture):
    leave = LeaveRequest.objects.create(employee=create_user_fixture, applied_on=datetime.date.today(),
                                        from_date=datetime.date(2022, 9, 18), to_date=datetime.date(2022, 9, 20),
                                        reason="For family trip")
    return leave


class TestUserModel:
    @pytest.mark.django_db
    def test_user1(self):
        User.objects.create_user('test1@gmail.com', 'test', 'user', '7894562314', date(2016, 9, 1),
                                 'FEMALE', 'Admin', 'Admin@123', password2='Admin@123')
        user = User.objects.filter(email='test1@gmail.com').exists()
        assert user

    @pytest.mark.django_db
    def test_user2(self):
        """
        Passwords don't match
        """
        User.objects.create_user('test1@gmail.com', 'test', 'user', '7894562314', date(2016, 9, 1),
                                 'FEMALE', 'Admin', 'Admin@123', password2='Admin123')
        user = User.objects.filter(email='test1@gmail.com').exists()
        assert not user

    @pytest.mark.django_db
    def test_user3(self):
        """
        Email not provided
        """
        user = User.objects.create_user(email='', first_name='test', last_name='user', contact='7894562314',
                                        birthdate=date(2016, 9, 1),
                                        gender='FEMALE', role='Admin', password='Admin@123', password2='Admin@123')
        assert type(user) == ValueError

    @pytest.mark.django_db
    def test_user4(self):
        """
        Role not provided
        """
        user = User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user',
                                        contact='7894562314',
                                        birthdate=date(2016, 9, 1),
                                        gender='FEMALE', role='', password='Admin@123', password2='Admin@123')
        assert type(user) == ValueError

    @pytest.mark.django_db
    def test_user5(self):
        User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user', contact='7894562314',
                                 birthdate=date(2016, 9, 1),
                                 gender='FEMALE', role='Doctor', password='Admin@123', password2='Admin@123')
        user = User.objects.get(email='test1@gmail.com')
        assert user.is_doctor

    @pytest.mark.django_db
    def test_user6(self):
        User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user', contact='7894562314',
                                 birthdate=date(2016, 9, 1),
                                 gender='FEMALE', role='Nurse', password='Admin@123', password2='Admin@123')
        user = User.objects.get(email='test1@gmail.com')
        assert user.is_nurse

    @pytest.mark.django_db
    def test_user7(self):
        User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user', contact='7894562314',
                                 birthdate=date(2016, 9, 1),
                                 gender='FEMALE', role='Surgeon', password='Admin@123', password2='Admin@123')
        user = User.objects.get(email='test1@gmail.com')
        assert user.is_surgeon

    @pytest.mark.django_db
    def test_user8(self):
        User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user', contact='7894562314',
                                 birthdate=date(2016, 9, 1),
                                 gender='FEMALE', role='Patient', password='Admin@123', password2='Admin@123')
        user = User.objects.get(email='test1@gmail.com')
        assert user.is_patient

    @pytest.mark.django_db
    def test_user9(self):
        User.objects.create_user(email='test1@gmail.com', first_name='test', last_name='user', contact='7894562314',
                                 birthdate=date(2016, 9, 1),
                                 gender='FEMALE', role='Receptionist', password='Admin@123', password2='Admin@123')
        user = User.objects.get(email='test1@gmail.com')
        assert user.is_receptionist

    @pytest.mark.django_db
    def test_email(self, create_user_fixture):
        user = create_user_fixture
        check_email = 'test1@gmail.com'
        assert user.email == check_email

    @pytest.mark.django_db
    def test_first_name(self, create_user_fixture):
        user = create_user_fixture
        first_name = 'test'
        assert user.first_name == first_name

    @pytest.mark.django_db
    def test_last_name(self, create_user_fixture):
        user = create_user_fixture
        last_name = 'user'
        assert user.last_name == last_name

    @pytest.mark.django_db
    def test_contact(self, create_user_fixture):
        user = create_user_fixture
        contact = '7894562314'
        assert user.contact == contact

    @pytest.mark.django_db
    def test_gender(self, create_user_fixture):
        user = create_user_fixture
        gender = 'FEMALE'
        assert user.gender == gender

    @pytest.mark.django_db
    def test_role(self, create_user_fixture):
        user = create_user_fixture
        role = 'Receptionist'
        assert user.role == role

    @pytest.mark.django_db
    def test_birthdate(self, create_user_fixture):
        user = create_user_fixture
        birthdate = date(2016, 9, 1)
        assert user.birthdate == birthdate

    @pytest.mark.django_db
    def test_is_admin(self, create_user_fixture):
        user = create_user_fixture
        assert not user.is_admin

    @pytest.mark.django_db
    def test_is_doctor(self, create_user_fixture):
        user = create_user_fixture
        assert not user.is_doctor

    @pytest.mark.django_db
    def test_is_nurse(self, create_user_fixture):
        user = create_user_fixture
        assert not user.is_nurse

    @pytest.mark.django_db
    def test_is_surgeon(self, create_user_fixture):
        user = create_user_fixture
        assert not user.is_surgeon

    @pytest.mark.django_db
    def test_is_patient(self, create_user_fixture):
        user = create_user_fixture
        assert not user.is_patient

    @pytest.mark.django_db
    def test_is_receptionist(self, create_user_fixture):
        user = create_user_fixture
        assert user.is_receptionist

    @pytest.mark.django_db
    def test_admin_user1(self):
        a = User.objects.create_superuser(email='test1@gmail.com', first_name='test', last_name='admin',
                                          contact='7894562314', birthdate=date(2016, 9, 1),
                                          gender='FEMALE',
                                          password='Admin@123',
                                          password2='Admin@123'
                                          )
        user = User.objects.filter(email='test1@gmail.com').exists()
        assert user


class TestShiftsModel:
    @pytest.mark.django_db
    def test_employee(self, create_shift_fixture, create_user_fixture):
        shift = create_shift_fixture
        assert shift.employee == create_user_fixture

    @pytest.mark.django_db
    def test_allocated_shift(self, create_shift_fixture):
        shift = create_shift_fixture
        assert shift.allocated_shift == 1

    @pytest.mark.django_db
    def test_shift_start(self, create_shift_fixture):
        shift = create_shift_fixture
        assert shift.shift_start == datetime.time(10, 0, 0)

    @pytest.mark.django_db
    def test_shift_end(self, create_shift_fixture):
        shift = create_shift_fixture
        assert shift.shift_end == datetime.time(10, 30, 0)

    @pytest.mark.django_db
    def test_allocated_place(self, create_shift_fixture):
        shift = create_shift_fixture
        assert shift.allocated_place == "OT"

    @pytest.mark.django_db
    def test_shift(self, create_user_fixture):
        employee = create_user_fixture
        shift = Shifts.objects.create(employee=employee, allocated_shift=2, shift_start=datetime.time(10, 0, 0),
                                      shift_end=datetime.time(10, 30, 0), allocated_place="OT")
        assert Shifts.objects.filter(employee=employee).exists()

    @pytest.mark.django_db
    def test_shift_str(self, create_user_fixture, create_shift_fixture):
        employee = create_user_fixture
        shift = create_shift_fixture
        print(str(shift))
        check_str = str(employee) + '-' + '1'
        assert str(shift) == check_str


class TestSubstitutionModel:
    @pytest.mark.django_db
    def test_shift_field(self, create_nurse_fixture, create_nurse_fixture2, create_substitution_fixture):
        shift, substitution = create_substitution_fixture
        assert substitution.shift == shift

    @pytest.mark.django_db
    def test_for_date_field(self, create_nurse_fixture, create_nurse_fixture2, create_substitution_fixture):
        shift, substitution = create_substitution_fixture
        assert substitution.for_date == datetime.date(2022, 9, 17)

    @pytest.mark.django_db
    def test_substitute_field(self, create_nurse_fixture, create_nurse_fixture2, create_substitution_fixture):
        shift, substitution = create_substitution_fixture
        assert substitution.substitute == create_nurse_fixture2

    @pytest.mark.django_db
    def test_str_field(self, create_nurse_fixture, create_nurse_fixture2, create_substitution_fixture):
        shift, substitution = create_substitution_fixture
        check_str = str(create_nurse_fixture2) + '-' + str(datetime.date(2022, 9, 17))
        assert str(substitution) == check_str

    @pytest.mark.django_db
    def test_substitution(self, create_nurse_fixture, create_nurse_fixture2):
        shift = Shifts.objects.create(employee=create_nurse_fixture, allocated_shift=1,
                                      shift_start=datetime.time(10, 0, 0),
                                      shift_end=datetime.time(10, 30, 0), allocated_place="A")
        substitution = Substitution.objects.create(shift=shift, for_date=datetime.date(2022, 9, 17),
                                                   substitute=create_nurse_fixture2)
        assert Substitution.objects.filter(id=substitution.id).exists()


class TestRoomModel:
    @pytest.mark.django_db
    def test_room(self):
        Rooms.objects.create(name="A", type="General", no_of_beds=5)
        assert Rooms.objects.filter(name="A").exists()

    @pytest.mark.django_db
    def test_name_field(self, create_room_fixture):
        room = create_room_fixture
        assert room.name == "A"

    @pytest.mark.django_db
    def test_type_field(self, create_room_fixture):
        room = create_room_fixture
        assert room.type == "General"

    @pytest.mark.django_db
    def test_no_of_beds_field(self, create_room_fixture):
        room = create_room_fixture
        assert room.no_of_beds == 5

    @pytest.mark.django_db
    def test_str(self, create_room_fixture):
        room = create_room_fixture
        assert str(room) == "A"


class TestLeaveRequestModel:
    @pytest.mark.django_db
    def test_employee_field(self, create_user_fixture, create_leave_request_fixture):
        leave = create_leave_request_fixture
        assert leave.employee == create_user_fixture

    @pytest.mark.django_db
    def test_applied_on_field(self, create_user_fixture, create_leave_request_fixture):
        leave = create_leave_request_fixture
        assert leave.applied_on == datetime.date.today()

    @pytest.mark.django_db
    def test_from_date_field(self, create_user_fixture, create_leave_request_fixture):
        leave = create_leave_request_fixture
        assert leave.from_date == datetime.date(2022, 9, 18)

    @pytest.mark.django_db
    def test_to_date_field(self, create_user_fixture, create_leave_request_fixture):
        leave = create_leave_request_fixture
        assert leave.to_date == datetime.date(2022, 9, 20)

    @pytest.mark.django_db
    def test_reason_field(self, create_user_fixture, create_leave_request_fixture):
        leave = create_leave_request_fixture
        assert leave.reason == "For family trip"

    @pytest.mark.django_db
    def test_leave_request(self, create_user_fixture):
        LeaveRequest.objects.create(employee=create_user_fixture, applied_on=datetime.date.today(),
                                    from_date=datetime.date(2022, 9, 18), to_date=datetime.date(2022, 9, 20),
                                    reason="For family trip")
        assert LeaveRequest.objects.filter(employee=create_user_fixture, applied_on=datetime.date.today())
