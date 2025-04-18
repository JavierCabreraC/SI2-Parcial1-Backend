from rest_framework import permissions



class IsAdminUser(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'admin'


class HasAdminRole(permissions.BasePermission):
    """
    Permiso que verifica si el token JWT contiene el rol 'admin'
    """
    def has_permission(self, request, view):
        # Obtiene el token decodificado del request
        if hasattr(request, 'auth') and isinstance(request.auth, dict):
            # Verifica si el token tiene un campo 'rol' con valor 'admin'
            return request.auth.get('rol') == 'admin'
        return False


class IsAlmacenista(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.rol == 'almacenista'

