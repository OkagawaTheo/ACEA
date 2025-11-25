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

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if hasattr(request.user, 'aluno') and obj.id_aluno == request.user.aluno:
                return True
        
        if request.user.is_superuser or hasattr(request.user, 'presidente') or hasattr(request.user, 'administrador'):
            return True
            
        return False