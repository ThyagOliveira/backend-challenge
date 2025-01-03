from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff
        
        if request.method == 'POST':
            return True
        
        return False


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return request.user and request.user.is_authenticated

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff

        return False
