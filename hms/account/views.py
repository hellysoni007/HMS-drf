from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .permissions import IsDoctor, IsNurse, IsSurgeon, IsReceptionist
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer
from .services import LoginRegisterUser


class UserRegistrationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        register_user = LoginRegisterUser.register_new_user(request)
        return register_user


class LoginView(APIView):

    def post(self, request, format=None):
        login = LoginRegisterUser.validate_credentials(request)
        return login


class HomeView(APIView):

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UsersListView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetailView(generics.RetrieveUpdateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class PatientListView(generics.ListAPIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request, format=None):
#         queryset = User.objects.filter(role="Patient")
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# class PatientCreateView(generics.CreateAPIView):
#     permission_classes = [IsReceptionist]
#
#     def post(self, request, format=None):
#         queryset = User.objects.filter(role="Patient")
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
