from rest_framework import permissions

class IsPresidenteOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            hasattr(request.user, 'presidente') 
        )

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and hasattr(request.user, 'professor')
        
        return False