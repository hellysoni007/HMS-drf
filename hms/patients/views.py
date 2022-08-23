from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from account.models import User
from account.permissions import IsReceptionist, IsDoctor, IsSurgeon, IsNurse
from .serializers import PatientRegistrationSerializer, PatientUpdateSerializer, ViewPatientSerializer


class PatientRegistrationView(generics.ListCreateAPIView):
    @permission_classes([IsReceptionist,IsDoctor,IsSurgeon,IsNurse])
    def get(self,request):
        queryset = User.objects.filter(role="Patient")
        serializer = ViewPatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsReceptionist])
    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role="Patient")
            return Response({'msg': 'Patient registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsReceptionist])
    def put(self, request, *args, **kwargs):
        queryset = User.objects.get(id=kwargs['pk'])
        print(queryset)
        serializer = PatientUpdateSerializer(queryset, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Patient details updated successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
