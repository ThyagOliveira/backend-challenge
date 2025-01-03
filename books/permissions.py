from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method in ['PUT', 'PATCH']:
            return request.user and request.user.is_staff
        
        if request.method == 'POST':
            return True
        
        return False