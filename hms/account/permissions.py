from rest_framework.permissions import BasePermission


def is_logged_in(request):

    try:
        role = request.user.role
        if role:
            return True
    except AttributeError:
        return False


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if is_logged_in(request):
            return request.user.role == "Doctor"
        else:
            return False


class IsSurgeon(BasePermission):
    def has_permission(self, request, view):
        if is_logged_in(request):
            return request.user.role == "Surgeon"
        else:
            return False


class IsNurse(BasePermission):
    def has_permission(self, request, view):
        if is_logged_in(request):
            return request.user.role == "Nurse"
        else:
            return False


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        if is_logged_in(request):
            return request.user.role == "Receptionist"
        else:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if is_logged_in(request):
            return request.user.role == "Admin"
        else:
            return False
