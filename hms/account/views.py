from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Shifts, LeaveRequest
from .permissions import IsDoctor, IsNurse, IsSurgeon, IsReceptionist, IsAdmin
from .queries import get_user_from_id, get_all_rooms
from .serializers import UserSerializer, RoomSerializer, ShiftsSerializer, LeaveRequestSerializer, \
    ShiftsUpdateSerializer
from .services import LoginRegisterUser, ManageShifts, MyShift, ManageProfile, MyLeaves, ManageLeaves, ManageSubstitute
from .tasks import email_service


class UserRegistrationView(APIView):
    permission_classes = [IsAdmin]
    """
    description: To register new employees
    params: first_name,last_name,email,contact,role,DOB,password,password2,gender (as request data)
    output: displays msg for registration success or fail
    """

    def post(self, request):
        register_user = LoginRegisterUser.register_new_user(request)
        return register_user


class LoginView(APIView):
    """
    description: Login view for all employees, return access token on successful login
    params: email,password
    output: login success msg
    """

    @staticmethod
    def post(request):
        login = LoginRegisterUser.validate_credentials(request)
        return login


class UsersListView(generics.ListAPIView):
    """
    description: View all users for admin
    params: None
    output: All users
    """
    permission_classes = [IsAdmin]
    queryset = User.objects.all().exclude(role='Admin').exclude(role='Patient')
    queryset = queryset.exclude(role='Patient')
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    description: retrieve or update users for Admin
    params: None
    output: success msg
    """
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeShiftView(generics.ListAPIView):
    """
    description: Show employee shift
    params: None
    output: shift details
    """
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse | IsAdmin]

    def get(self, request, *args, **kwargs):
        view_shift = MyShift.view_shift(request)
        return view_shift


class ShiftCreateView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsAdmin]

    """
    Assign shifts to new employees.
    """

    def post(self, request, *args, **kwargs):
        """
        description: Assign shifts to new employees.
        params: pk(employee id)
        output: success msg
        """
        user = get_user_from_id(kwargs['pk'])
        add_shift = ManageShifts.add_shift_user(request, user, user_id=kwargs['pk'])
        return add_shift

    def put(self, request, *args, **kwargs):
        """
        description: Assign shifts to new employees.
        params: pk(employee id)
        output: success msg
        """
        employee = kwargs['pk']
        try:
            queryset = Shifts.objects.get(employee=employee)
        except Shifts.DoesNotExist:
            return Response({'msg': 'Employee does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShiftsUpdateSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            shift = serializer.save()
            mail_msg = f'Hello {shift.employee.first_name},\nYour new shift details are as follows:\nShift start ' \
                       f'time:' \
                       f'{shift.shift_start}\nShift End time: {shift.shift_end}\nAllocated place: ' \
                       f'{shift.allocated_place}'
            print(mail_msg)
            email_service.delay([shift.employee.email], "Your shift has been changed", mail_msg)
            return Response({'msg': 'Shift updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        description: Display shifts of all employees.
        params: pk(employee id)(optional)
        output: display shift or particular shift
        """
        if kwargs:
            employee = kwargs['pk']
            queryset = Shifts.objects.filter(employee=employee)
            if not queryset:
                return Response({'msg': 'Employee does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Shifts.objects.all()
        serializer = ShiftsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomCreateView(generics.ListCreateAPIView):
    """
    Create new rooms, access only to Admins
    """
    queryset = get_all_rooms()
    serializer_class = RoomSerializer
    permission_classes = [IsAdmin]


class RoomUpdateView(generics.RetrieveUpdateAPIView):
    """
    Create new rooms, access only to Admins
    """
    queryset = get_all_rooms()
    serializer_class = RoomSerializer
    permission_classes = [IsAdmin]


class ViewProfileView(generics.UpdateAPIView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    """
    All employees on login can update or view profile
    """

    def get(self, request, *args, **kwargs):
        """
        description: View log in user profile
        params: None
        output: profile details
        """
        view_profile = ManageProfile.view_user_profile(request)
        return view_profile

    def put(self, request, *args, **kwargs):
        """
        description: Update log in user profile
        params: None
        output: profile details
        """
        update_profile = ManageProfile.update_user_profile(request)

        return update_profile


class MonthlyScheduleView(generics.ListAPIView):
    """
    View full month schedule for all employees
    """
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        """
        description: View log in users monthly schedule
        params: None
        output: monthly schedule
        """
        monthly_schedule = MyShift.monthly_schedule(request)
        return monthly_schedule


class LeaveListCreateView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]
    """
    Post leave request, update leave requests, view leave requests for employees
    """

    def get(self, request, *args, **kwargs):
        """
        description: View log in users leaves
        params: leave_id
        output: leaves or leave details
        """
        show_leaves = MyLeaves.view_leave(request, kwargs)
        return show_leaves

    def post(self, request, *args, **kwargs):
        """
        description: Add new leave request
        params: None
        output: success or failure msg
        """
        apply_for_leave = MyLeaves.apply_leave(request)
        return apply_for_leave

    def put(self, request, *args, **kwargs):
        """
        description: Update leave request
        params: leave_id
        output: success or failure msg
        """
        apply_for_leave = MyLeaves.update_leave(request, kwargs['pk'])
        return apply_for_leave


class LeaveDeleteView(generics.UpdateAPIView):
    """
    Delete leave request for all employees
    """
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def put(self, request, *args, **kwargs):
        """
        description: Delete leave request
        params: leave_id
        output: success or failure msg
        """
        delete_leave = MyLeaves.delete_leave(request, kwargs['pk'])
        return delete_leave


class LeaveApprovalView(generics.ListAPIView, generics.UpdateAPIView):
    """
    Approve Disapprove leaves for Admin, View all leaves for admin
    """
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: View all users leaves
        params: leave_id
        output: leaves or leave detail
        """
        leaves = ManageLeaves.view_leaves(kwargs, request)
        return leaves

    def put(self, request, *args, **kwargs):
        """
        description: Approve or Disapprove leaves
        params: leave_id
        output: success or failure msg
        """
        leave_approval = ManageLeaves.approve_disapprove_leave(kwargs, request)
        return leave_approval


class GetLatestLeavesViews(generics.ListAPIView):
    """
    Get the latest leaves to be reviewed for admin
    """
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: Get latest leaves
        params: None
        output: latest leaves
        """
        queryset = LeaveRequest.objects.filter(status="REQUESTED", is_delete=False).order_by('-applied_on')
        serializer = LeaveRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NeedSubstitution(generics.ListAPIView):
    """
    Get the leaves that need a substitute employee for admin
    """
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: Get leaves that are approved and need a subsitute
        params: None
        output: leaves
        """
        need_substitute = ManageSubstitute.view_need_of_substitute()
        return need_substitute


class AssignSubstituteDuty(generics.ListAPIView, generics.CreateAPIView):
    """
    Assign substitute duty to employees for admin
    """
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        """
        description: Get all substitutes details
        params: None
        output: substitutes
        """
        substitutions = ManageSubstitute.view_all_substitution()
        return substitutions

    def post(self, request, *args, **kwargs):
        """
        description: Assign substitute duty
        params: leave_id
        output: success or failure msg
        """
        substitution = ManageSubstitute.assign_substitution(kwargs, request)
        return substitution
