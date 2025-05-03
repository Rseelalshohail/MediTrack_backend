from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin')

class IsEngineerUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'engineer')

class IsNurseUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'nurse')

class IsAdminOrNurse(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin') or hasattr(request.user, 'nurse')

class IsAdminOrEngineer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin') or hasattr(request.user, 'engineer')
