from rest_framework.permissions import BasePermission


class IsFarmer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'


class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'investor'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsConsumer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'consumer'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'


class IsFarmerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('farmer', 'admin')


class IsInvestorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('investor', 'admin')
