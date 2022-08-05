from rest_framework.permissions import BasePermission, IsAdminUser


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Doctor"


class IsSurgeon(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Surgeon"


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Nurse"


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Receptionist"
