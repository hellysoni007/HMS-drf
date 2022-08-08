import datetime
import calendar

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Shifts, Rooms, User, Address
from .queries import get_user_from_mail
from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    AddressSerializer,
    ShiftsSerializer,
    UserSerializer)


def get_method_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def add_address(request, user):
    address_serializer = AddressSerializer(data=request.data)
    if address_serializer.is_valid(raise_exception=True):
        def perform_create(address):
            address.save(user=user)

        perform_create(address_serializer)
    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_employee_to_room(user, allocated_place):
    get_room = Rooms.objects.get(name=allocated_place)
    get_room.assigned_nurses.add(user)
    get_room.save()
    return get_room


def get_days_to_display():
    today_date = datetime.date.today()
    today_day = today_date.day
    month_last_day = calendar.monthrange(today_date.year, today_date.month)[1]
    return today_day, month_last_day


def create_next_week_schedule(request):
    today_day, month_last_day = get_days_to_display()
    view_shift = MyShift.view_shift(request)
    shift = []
    for i in range(today_day, month_last_day):
        daily_shifts = dict()
        daily_shifts['Date'] = datetime.date(year=datetime.date.today().year,
                                             month=datetime.date.today().month,
                                             day=i)
        daily_shifts['Shift-details'] = view_shift.data
        shift.append(daily_shifts)
    return shift


def get_available_rooms():
    rooms = Rooms.objects.all()
    available_shifts_places = []
    for room in rooms:
        counts = room.get_available_shifts_nurses()
        if counts <= 2:
            available_shifts_places.append(room)

    return available_shifts_places


def check_user_already_has_shift(user):
    return Shifts.objects.filter(employee=user).exists()


class LoginRegisterUser:

    @staticmethod
    def register_new_user(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            add_address(request, user)
            return Response({'msg': 'Registration Successful'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def validate_credentials(request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_method_for_user(user)
                return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageShifts:
    @staticmethod
    def add_shift_user(new_request, user):
        if get_available_rooms():
            if new_request.data['allocated_place'] not in get_available_rooms():
                return Response({'msg': 'Allocated room already has required staff.'})

        if not check_user_already_has_shift(user):
            shift_serializer = ShiftsSerializer(data=new_request.data)
            if shift_serializer.is_valid(raise_exception=True):
                def perform_create(shift):
                    shift.save(employee=user)

                perform_create(shift_serializer)
                add_employee_to_room(user, new_request.data['allocated_place'])
                return Response({'msg': 'Employee has been assigned the shift.'})
            return Response(shift_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Employee already has assigned shift.'})


class MyShift:
    @staticmethod
    def view_shift(request):
        queryset = Shifts.objects.get(employee=request.user)
        shift_serializer = ShiftsSerializer(queryset)
        shift_data = shift_serializer.data
        return Response(shift_data, status=status.HTTP_200_OK)

    @staticmethod
    def monthly_schedule(request):
        view_shift = create_next_week_schedule(request)
        queryset = User.objects.get(id=request.user.id)
        serializer = UserSerializer(queryset)
        create_next_week_schedule(request)
        return Response({'User': serializer.data, 'User-shift': view_shift}, status=status.HTTP_200_OK)


class ManageProfile:
    @staticmethod
    def view_user_profile(request):
        queryset = get_user_from_mail(request.user)
        serializer = UserSerializer(queryset)
        queryset2 = Address.objects.get(user=queryset.id)
        serializer2 = AddressSerializer(queryset2)

        return Response({'Profile Details': serializer.data, 'Address': serializer2.data}, status=status.HTTP_200_OK)

    @staticmethod
    def update_user_profile(request):
        queryset = get_user_from_mail(request.user)
        serializer = UserSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Profile updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_user_address_profile(request):
        queryset = get_user_from_mail(request.user)
        queryset2 = Address.objects.get(user=queryset.id)
        serializer2 = AddressSerializer(queryset2, data=request.data, partial=True)
        if serializer2.is_valid(raise_exception=True):
            serializer2.save()
            return Response({'msg': 'Address updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
