from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, contact, birthdate, gender, role,password, joining_date=None,
                    qualifications=None, speciality=None,
                    experiance_in_years=None,password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name, contact, birthdate, gender,role, joining_date,
        qualifications (if any), speciality(if any),experiance_in_years(if any), password.

        """
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

    def create_superuser(self, email, first_name, last_name, contact, birthdate, gender,password):
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
    age = models.IntegerField(null=True,blank=True)
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

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
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
