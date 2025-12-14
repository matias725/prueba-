from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: Solo admin puede crear/editar/eliminar
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado: Solo admin
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOperador(permissions.BasePermission):
    """
    Permiso personalizado: Solo operador o admin (lectura)
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user and request.user.is_staff
        return True
