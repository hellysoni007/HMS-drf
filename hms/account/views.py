from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Shifts, LeaveRequest
from .permissions import IsDoctor, IsNurse, IsSurgeon, IsReceptionist
from .queries import get_user_from_id, get_all_rooms
from .serializers import UserSerializer, RoomSerializer, ShiftsSerializer, LeaveRequestSerializer
from .services import LoginRegisterUser, ManageShifts, MyShift, ManageProfile, MyLeaves, ManageLeaves, ManageSubstitute


class UserRegistrationView(APIView):
    """
    Registration of new employees, permission class IsAdminUser allows only admin to register new employees.
    """

    @permission_classes([IsAdminUser])
    def post(self, request):
        register_user = LoginRegisterUser.register_new_user(request)
        return register_user


class LoginView(APIView):
    """
    Login view for all employees, return access token on successful login
    """

    @staticmethod
    def post(request):
        login = LoginRegisterUser.validate_credentials(request)
        return login


class UsersListView(generics.ListAPIView):
    """
    View all users for Admin
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().exclude(role='Admin')
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    retrieve or update users for Admin
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmployeeShiftView(generics.ListAPIView):
    """
    All employees and admin has permission to view their shifts
    """
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse | IsAdminUser]

    def get(self, request, *args, **kwargs):
        view_shift = MyShift.view_shift(request)
        return view_shift


class ShiftCreateView(generics.ListCreateAPIView):
    """
    Assign shifts to new employees.
    """

    @permission_classes([IsAdminUser])
    def post(self, request, *args, **kwargs):
        user = get_user_from_id(kwargs['pk'])
        add_shift = ManageShifts.add_shift_user(request, user, user_id=kwargs['pk'])
        return add_shift

    @permission_classes([IsAdminUser])
    def get(self, request, *args, **kwargs):
        queryset = Shifts.objects.all()
        serializer = ShiftsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomCreateView(generics.ListCreateAPIView):
    """
    Create new rooms, access only to Admins
    """
    queryset = get_all_rooms()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]


class RoomUpdateView(generics.RetrieveUpdateAPIView):
    """
    Create new rooms, access only to Admins
    """
    queryset = get_all_rooms()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]


class ViewProfileView(APIView):
    """
    All employees on login can update or view profile
    """

    @permission_classes([IsAuthenticated])
    def get(self, request):
        view_profile = ManageProfile.view_user_profile(request)
        return view_profile

    @permission_classes([IsAuthenticated])
    def put(self, request):
        update_profile = ManageProfile.update_user_profile(request)

        return update_profile


class MonthlyScheduleView(generics.ListAPIView):
    """
    View full month schedule for all employees
    """
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        monthly_schedule = MyShift.monthly_schedule(request)
        return monthly_schedule


class LeaveListCreateView(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def get(self, request, *args, **kwargs):
        show_leaves = MyLeaves.view_leave(request, kwargs)
        return show_leaves

    def post(self, request, *args, **kwargs):
        apply_for_leave = MyLeaves.apply_leave(request)
        return apply_for_leave

    def put(self, request, *args, **kwargs):
        apply_for_leave = MyLeaves.update_leave(request, kwargs['pk'])
        return apply_for_leave


class LeaveDeleteView(generics.UpdateAPIView):
    permission_classes = [IsReceptionist | IsDoctor | IsSurgeon | IsNurse]

    def put(self, request, *args, **kwargs):
        delete_leave = MyLeaves.delete_leave(request, kwargs['pk'])
        return delete_leave


class LeaveApprovalView(generics.ListAPIView, generics.UpdateAPIView):
    @permission_classes([IsAdminUser])
    def get(self, request, *args, **kwargs):
        leaves = ManageLeaves.view_leaves(kwargs, request)
        return leaves

    @permission_classes([IsAdminUser])
    def put(self, request, *args, **kwargs):
        leave_approval = ManageLeaves.approve_disapprove_leave(kwargs, request)
        return leave_approval


class GetLatestLeavesViews(generics.ListAPIView):
    @permission_classes([IsAdminUser])
    def get(self, request, *args, **kwargs):
        queryset = LeaveRequest.objects.filter(status="REQUESTED", is_delete=False).order_by('-applied_on')
        serializer = LeaveRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NeedSubstitution(generics.ListAPIView):

    @permission_classes([IsAdminUser])
    def get(self, request, *args, **kwargs):
        need_substitute = ManageSubstitute.view_need_of_substitute()
        return need_substitute


class AssignSubstituteDuty(generics.ListAPIView, generics.CreateAPIView):

    @permission_classes([IsAdminUser])
    def get(self, request, *args, **kwargs):
        substitutions = ManageSubstitute.view_all_substitution()
        return substitutions

    @permission_classes([IsAdminUser])
    def post(self, request, *args, **kwargs):
        substitution = ManageSubstitute.assign_substitution(kwargs, request)
        return substitution
