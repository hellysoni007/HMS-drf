import datetime
import calendar

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Shifts, Rooms, User, Address, LeaveRequest, Substitution
from .queries import get_user_from_mail, get_address_from_user_id, get_user_from_id
from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    AddressSerializer,
    ShiftsSerializer,
    UserSerializer, LeavesSerializer, LeaveRequestSerializer, GetSubstitutionSerializer, SubstitutionSerializer)


def get_dates(start, end):
    step = datetime.timedelta(days=1)
    date_list = []
    while start <= end:
        if start > datetime.date.today():
            date_list.append(str(start))
        start += step
    return date_list


def substitute_on_leave(employee_id, date_check):
    substitute_leaves = LeaveRequest.objects.filter(employee=employee_id, is_delete=False)
    dates = []
    for leave in substitute_leaves:
        start = leave.from_date
        end = leave.to_date
        dates = dates + get_dates(start, end)
    if date_check in dates:
        return True
    else:
        return False


def get_method_for_user(user):
    """
    :param user:
    :return generated token:
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def add_address(request, user):
    """
    Add address(request.data) for user(user)
    :param request:
    :param user:
    :return errors(if Any):
    """
    address_serializer = AddressSerializer(data=request.data)
    if address_serializer.is_valid(raise_exception=True):
        def perform_create(address):
            address.save(user=user)

        perform_create(address_serializer)
    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_employee_to_room(user, allocated_place):
    """
    Allocate room(allocated_place) to employee(user)
    :param user:
    :param allocated_place:
    :return room allocated:
    """
    get_room = Rooms.objects.get(name=allocated_place)
    get_room.assigned_nurses.add(user)
    get_room.save()
    return get_room


def get_days_to_display():
    """
    Get today's day and last day of this month
    :return today's day and last day of the current month:
    """
    today_date = datetime.date.today()
    today_day = today_date.day
    month_last_day = calendar.monthrange(today_date.year, today_date.month)[1]
    return today_day, month_last_day


def get_leaves_list(request):
    leaves = LeaveRequest.objects.filter(employee=request.user.id, is_delete=False)
    leaves_dates = []
    for leave in leaves:
        leave_start_date = leave.from_date
        leave_end_date = leave.to_date
        delta = datetime.timedelta(days=1)
        while leave_start_date <= leave_end_date:
            print(leave_end_date.strftime("%Y-%m-%d"))
            leaves_dates.append(leave_end_date)
            leave_start_date += delta
    print(leaves_dates)
    return leaves_dates


def check_is_substitute(check_date, request):
    try:
        is_substitute = Substitution.objects.get(for_date=check_date, substitute=request.user.id)
        if is_substitute:
            print(f'substitution shift: {is_substitute.shift.id}')
            return is_substitute.shift.id
    except Substitution.DoesNotExist:
        return None


def get_substitute_shift(shift_id):
    print(shift_id)
    queryset = Shifts.objects.get(id=shift_id)
    serializer = ShiftsSerializer(queryset)
    return serializer.data


def create_next_month_schedule(request):
    today_day, month_last_day = get_days_to_display()
    view_shift = MyShift.view_shift(request)
    shift = []
    leaves_dates = get_leaves_list(request)
    for i in range(today_day, month_last_day):
        daily_shifts = dict()
        date = datetime.date(year=datetime.date.today().year,
                             month=datetime.date.today().month,
                             day=i)
        daily_shifts['Date'] = date
        if check_is_substitute(date, request):
            sub_shift = get_substitute_shift(check_is_substitute(date, request))
            daily_shifts['Shift-details'] = sub_shift

        elif date in leaves_dates:
            daily_shifts['Shift-details'] = "Leave"
        else:
            daily_shifts['Shift-details'] = view_shift.data
        shift.append(daily_shifts)
    print(shift)
    return shift


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
    def add_shift_user(new_request, user, user_id):
        if not check_user_already_has_shift(user):
            new_request.data['employee'] = user_id
            shift_serializer = ShiftsSerializer(data=new_request.data)
            if shift_serializer.is_valid(raise_exception=True):
                shift_serializer.save()
                if user.role == 'Nurse':
                    add_employee_to_room(user, new_request.data['allocated_place'])
                return Response({'msg': 'Employee has been assigned the shift successfully.'})
            return Response(shift_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Employee already has been assigned shift.'})


def check_is_substitute_today(request):
    today = datetime.date.today()
    is_substitute = Substitution.objects.filter(substitute=request.user.id, for_date=today)
    if is_substitute:
        is_substitute = Substitution.objects.get(substitute=request.user.id, for_date=today)
        shift_data = Shifts.objects.get(id=is_substitute.shift.id)
        shift_serializer = ShiftsSerializer(shift_data)
        substitute_shift_data = shift_serializer.data
        in_place = substitute_shift_data.pop("employee")
        substitute_shift_data["In Place Of"] = in_place
        data = {"substitute_shift": substitute_shift_data}
        return data
    else:
        print(False)


class MyShift:
    @staticmethod
    def view_shift(request):
        queryset = Shifts.objects.get(employee=request.user)
        shift_serializer = ShiftsSerializer(queryset)
        shift_data = shift_serializer.data
        if check_is_substitute_today(request):
            substitute_data = check_is_substitute_today(request)
            return Response({"Regular Shift": shift_data, "Substitute Shift": substitute_data},
                            status=status.HTTP_200_OK)
        return Response(shift_data, status=status.HTTP_200_OK)

    @staticmethod
    def monthly_schedule(request):
        view_shift = create_next_month_schedule(request)
        queryset = User.objects.get(id=request.user.id)
        serializer = UserSerializer(queryset)
        create_next_month_schedule(request)
        return Response({'User': serializer.data, 'Month-schedule': view_shift}, status=status.HTTP_200_OK)


class ManageProfile:
    @staticmethod
    def view_user_profile(request):
        queryset = get_user_from_mail(request.user)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def update_user_profile(request):
        user_queryset = get_user_from_mail(request.user)
        serializer = UserSerializer(user_queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                address_queryset = get_address_from_user_id(user_queryset.id)
                if not address_queryset:
                    Address.objects.create(user=request.user)
            except AttributeError as e:
                address_queryset = get_address_from_user_id(user_queryset.id)
            address_serializer = AddressSerializer(address_queryset, data=request.data, partial=True)
            if address_serializer.is_valid(raise_exception=True):
                address_serializer.save()
                return Response({'msg': 'Profile updated successfully.'}, status=status.HTTP_201_CREATED)
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyLeaves:
    @staticmethod
    def apply_leave(request):
        user = get_user_from_mail(request.user)
        serializer = LeavesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(employee=user)
            return Response({'msg': 'Leave applied successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def view_leave(request, kwargs):
        if kwargs:
            try:
                my_leaves = LeaveRequest.objects.get(id=kwargs['pk'], employee=request.user)
                serializer = LeavesSerializer(my_leaves)
            except LeaveRequest.DoesNotExist as e:
                my_leaves = LeaveRequest.objects.filter(employee=request.user)
                serializer = LeavesSerializer(my_leaves, many=True)
        else:
            queryset = LeaveRequest.objects.filter(employee=request.user)
            serializer = LeavesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def update_leave(request, leave_id):
        try:
            queryset = LeaveRequest.objects.get(id=leave_id)
            if queryset.employee != request.user:
                return Response({'msg': 'Cannot update others leaves.'},
                                status=status.HTTP_201_CREATED)
            if queryset.status != "REQUESTED":
                return Response({'msg': 'The Leave request can not be updated as it has been reviewed.'},
                                status=status.HTTP_201_CREATED)
            serializer = LeavesSerializer(queryset, data=request.data, partial=True)
        except LeaveRequest.DoesNotExist as e:
            print(e)
            return Response({'msg': 'No leave application found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Leave updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_leave(request, leave_id):
        try:
            today = datetime.date.today()
            queryset = LeaveRequest.objects.get(id=leave_id)
            if queryset.employee != request.user:
                return Response({'msg': 'Cannot delete others leaves.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if queryset.from_date >= today:
                return Response({'msg': 'The Leave request can not be deleted once date has passed.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except LeaveRequest.DoesNotExist as e:
            print(e)
            return Response({'msg': 'No leave application found'}, status=status.HTTP_404_NOT_FOUND)
        queryset.is_delete = True
        queryset.save()
        return Response({'msg': 'Leave request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


def get_all_dates(start, end):
    step = datetime.timedelta(days=1)
    date_list = []
    while start <= end:
        date_list.append(str(start))
        start += step
    return date_list


def get_leaves_for_date(check_date, queryset):
    leaves = []
    for query in queryset:
        start = query.from_date
        end = query.to_date
        dates = get_all_dates(start, end)
        if check_date in dates:
            leaves.append(query)
    return leaves


class ManageLeaves:
    @staticmethod
    def view_leaves(kwargs, request):
        if kwargs:
            queryset = LeaveRequest.objects.get(id=kwargs['pk'])
            serializer = LeaveRequestSerializer(queryset)
        elif request.data:
            queryset = LeaveRequest.objects.filter(status="ACCEPTED")
            leaves = get_leaves_for_date(request.data['date'], queryset)
            serializer = LeaveRequestSerializer(leaves, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = LeaveRequest.objects.all()
            serializer = LeaveRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def approve_disapprove_leave(kwargs, request):
        try:
            queryset = LeaveRequest.objects.get(id=kwargs['pk'])
        except LeaveRequest.DoesNotExist as e:
            return Response({'msg': 'No leave application found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveRequestSerializer(queryset, data=request.data, partial=True)
        print(queryset.status)
        if queryset.status == 'ACCEPTED':
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if request.data['status'] == 'ACCEPTED':
                    return Response({'msg': 'Leave approved.'}, status=status.HTTP_201_CREATED)
                elif request.data['status'] == 'REJECTED':
                    return Response({'msg': 'Leave rejected.'}, status=status.HTTP_201_CREATED)
        elif queryset.status == 'REJECTED':
            return Response({'msg': 'Please ask employee to send another request.'}, status=status.HTTP_201_CREATED)
        else:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if request.data['status'] == 'ACCEPTED':
                    return Response({'msg': 'Leave approved.'}, status=status.HTTP_201_CREATED)
                elif request.data['status'] == 'REJECTED':
                    return Response({'msg': 'Leave rejected.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageSubstitute:
    @staticmethod
    def view_need_of_substitute():
        queryset = LeaveRequest.objects.filter(has_substitute=False, status="ACCEPTED", is_delete=False)
        serializer = LeaveRequestSerializer(queryset, many=True)
        print(serializer.data)
        return Response({'Leaves left to assign substitute.': serializer.data}, status=status.HTTP_200_OK)

    @staticmethod
    def view_all_substitution():
        queryset = Substitution.objects.all()
        serializer = GetSubstitutionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def assign_substitution(kwargs, request):
        leave_id = kwargs['pk']
        get_leave = LeaveRequest.objects.get(id=leave_id)
        request.data['leave'] = get_leave
        employee = get_leave.employee
        get_shift = Shifts.objects.get(employee=employee)
        request.data['shift'] = get_shift.id
        get_leaves_dates = get_dates(get_leave.from_date, get_leave.to_date)
        check_date = request.data['for_date']
        if check_date not in get_leaves_dates:
            return Response({'msg': "No leaves approved for this date"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubstitutionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            get_leave.has_substitute = True
            get_leave.save()
            return Response({'msg': 'Substitution done successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
