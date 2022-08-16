from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, contact, birthdate, gender, role, password, joining_date=None,
                    qualifications=None, speciality=None,
                    experiance_in_years=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name,
         contact, birthdate, gender,role, joining_date,
        qualifications (if any), speciality(if any),experiance_in_years(if any), password.

        """
        if password != password2:
            return ValueError('Password and check password does not match')
        if not email:
            raise ValueError('Users must have an email address')

        if not role:
            raise ValueError('Users must have a role')

        if role == 'Doctor':
            is_doctor = True
        else:
            is_doctor = False
        if role == 'Nurse':
            is_nurse = True
        else:
            is_nurse = False
        if role == 'Surgeon':
            is_surgeon = True
        else:
            is_surgeon = False
        if role == 'Receptionist':
            is_receptionist = True
        else:
            is_receptionist = False
        if role == 'Patient':
            is_patient = True
        else:
            is_patient = False
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            birthdate=birthdate,
            gender=gender,
            role=role,
            joining_date=joining_date,
            is_doctor=is_doctor,
            is_surgeon=is_surgeon,
            is_nurse=is_nurse,
            is_receptionist=is_receptionist,
            is_patient=is_patient,
            qualifications=qualifications,
            speciality=speciality,
            experiance_in_years=experiance_in_years
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, contact, birthdate, gender, password):
        """
        Creates and saves a superuser with the given email, first_name,last_name and password.
        """
        role = 'Admin'
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            birthdate=birthdate,
            gender=gender,
            role=role
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = [('MALE', 'MALE'), ('FEMALE', 'FEMALE')]
    ROLE_CHOICES = [('Doctor', 'Doctor'),
                    ('Nurse', 'Nurse'),
                    ('Surgeon', 'Surgeon'),
                    ('Receptionist', 'Receptionist'),
                    ('Patient', 'Patient'),
                    ('Admin', 'Admin')]

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    contact = models.CharField(max_length=12, null=False, blank=False)
    birthdate = models.DateField(verbose_name="DOB", null=False, blank=False)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
    )
    role = models.CharField(
        max_length=12,
        choices=ROLE_CHOICES
    )
    joining_date = models.DateField(blank=True, null=True)
    termination_date = models.DateTimeField(blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_surgeon = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_active = True
    qualifications = models.CharField(max_length=200, blank=True, null=True)
    speciality = models.CharField(max_length=200, null=True, blank=True)
    experiance_in_years = models.IntegerField(verbose_name='Experiance(in yrs)', null=True, blank=True)
    leaves_taken = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact', 'birthdate', 'gender']

    def __str__(self):
        return self.email

    def has_perm(self):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    @staticmethod
    def has_module_perms():
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        if self.is_patient:
            return False
        else:
            return True


class Address(models.Model):
    user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
    block_no = models.CharField(max_length=10, verbose_name="Block No./ Flat No.", null=True, blank=True)
    building_name = models.CharField(verbose_name="Flat Name, Society Name", max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user


class Shifts(models.Model):
    # Let shift 1 be from 8 a.m to 3.59 p.m
    # Let shift 2 be from 4 p.m to 11.59 a.m
    # Let shift 1 be from 0 a.m to 7.59 a.m
    SHIFTS = [('1', '1'), ('2', '2'), ('3', '3')]
    employee = models.ForeignKey(User, related_name='shift', on_delete=models.CASCADE)
    allocated_shift = models.CharField(max_length=1, choices=SHIFTS)
    # date = models.DateField(null=True,blank=True)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    allocated_place = models.CharField(verbose_name='Allocated duty', max_length=20, blank=False, null=False)

    def __str__(self):
        return f'{self.employee}-{self.allocated_shift}'

    def if_proxy(self):
        pass

    def add_nurses_to_rooms(self):
        employee_object = User.objects.get(id=self.employee)
        if employee_object.role == 'Nurse':
            room_allocated = self.allocated_place
            room = Rooms.objects.get(name=room_allocated)
            room.assigned_nurses.add(self.employee)
            room.save()
            return self


class Rooms(models.Model):
    TYPES_OF_ROOMS = [('General', 'General'), ('Special', 'Special')]
    name = models.CharField(max_length=5, null=False, blank=False, unique=True)
    type = models.CharField(max_length=7, choices=TYPES_OF_ROOMS, null=True, blank=True)
    no_of_beds = models.IntegerField(null=False, blank=False)
    assigned_nurses = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_available_shifts_nurses(self):
        return self.assigned_nurses.all().count()


class LeaveRequest(models.Model):
    STATUS_CHOICES = [('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('REQUESTED', 'REQUESTED')]
    employee = models.ForeignKey(User, related_name='leaves', on_delete=models.CASCADE)
    applied_on = models.DateField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='REQUESTED')

    class Meta:
        ordering = ['-from_date', 'applied_on']

    def __str__(self):
        return self.employee

    # def get_employees_on_leave_today(self):
    #     LeaveRequest.objects.get()
