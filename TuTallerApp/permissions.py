from rest_framework.permissions import BasePermission


class BaseRolPermission(BasePermission):
    rol_permitido = None

    def has_permission(self, request, view):
        user = request.user

        # 🔒 Seguridad extra
        if not user or not user.is_authenticated:
            return False

        rol = getattr(user, "rol", None)

        if not rol or not rol.nombre:
            return False

        return rol.nombre.lower() == self.rol_permitido


class EsCliente(BaseRolPermission):
    rol_permitido = "cliente"


class EsEmpresa(BaseRolPermission):
    rol_permitido = "empresa"


class EsAdmin(BaseRolPermission):
    rol_permitido = "admin"