# urls.py (APP)

from django.urls import path


from .views import horarios_disponibles
from .views import obtener_agendas
# AUTH
from .auth_api import (
    RegistroAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
    PerfilAPIView,
    CambiarPasswordAPIView,
    LogoutAPIView,ActualizarPerfilAPIView, EliminarCuentaAPIView
)

# CORE API
from .api import (
    EstablecimientoListAPIView,
    EstablecimientoDetailAPIView,
    EstablecimientoCreateAPIView,
    ServiciosPorEstablecimientoAPIView,
    ServicioCreateAPIView,
    VehiculoCreateAPIView,
    MisVehiculosAPIView,
    CrearCitaAPIView,
    MisCitasAPIView,EstablecimientosRecomendadosAPIView,
    CitasEmpresaAPIView,
    CambiarEstadoCitaAPIView,
    CrearCalificacionAPIView,
    CalificacionesEstablecimientoAPIView,
    DashboardEmpresaAPIView,
    MisNotificacionesAPIView,
    MarcarLeidaAPIView,EliminarCitaAPIView,TopEstablecimientosAPIView,
    HorariosDisponiblesAPIView,
    DetalleMiCitaAPIView,
    RolesPublicosAPIView,
    CrearResenaAPIView,
    MisResenasAPIView,
    AnunciosAPIView,
)
from .admin_api import (
    UsuarioListCreateView,
    UsuarioRetrieveUpdateDestroyView,
    VehiculoListCreateView,
    VehiculoRetrieveUpdateDestroyView,
    ServicioListCreateView,
    ServicioRetrieveUpdateDestroyView,
    PrestacionListCreateView,
    PrestacionRetrieveUpdateDestroyView,
    CalificacionListCreateView,
    CalificacionRetrieveUpdateDestroyView,
    NotificacionListCreateView,
    NotificacionRetrieveUpdateDestroyView,
    
)

urlpatterns = [
    
    # 🧩 ROLES
    path('roles/', RolesPublicosAPIView.as_view()),

    # 📢 ANUNCIOS
    path('anuncios/', AnunciosAPIView.as_view()),

    # 🔐 AUTH
    path('auth/register/', RegistroAPIView.as_view()),
    path('usuarios/register/', RegistroAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('auth/logout/', LogoutAPIView.as_view()),
    path('auth/perfil/', PerfilAPIView.as_view()),
    path('auth/cambiar-password/', CambiarPasswordAPIView.as_view()),
    path('auth/perfil/actualizar/', ActualizarPerfilAPIView.as_view()),
    path('auth/eliminar/', EliminarCuentaAPIView.as_view()),

    # 🏢 ESTABLECIMIENTOS
    path('establecimientos/', EstablecimientoListAPIView.as_view()),
    path('establecimientos/<int:pk>/', EstablecimientoDetailAPIView.as_view()),
    path('establecimientos/crear/', EstablecimientoCreateAPIView.as_view()),
    path('establecimientos/top/', TopEstablecimientosAPIView.as_view()),
    path('recomendados/', EstablecimientosRecomendadosAPIView.as_view()),

    # 🛠 SERVICIOS
    path('servicios/establecimiento/<int:establecimiento_id>/', ServiciosPorEstablecimientoAPIView.as_view()),
    path('servicios/crear/', ServicioCreateAPIView.as_view()),

    # 🚗 VEHÍCULOS
    path('vehiculos/', MisVehiculosAPIView.as_view()),
    path('vehiculos/crear/', VehiculoCreateAPIView.as_view()),

    # 📅 CITAS (CLIENTE)
    path('citas/', MisCitasAPIView.as_view()),               # GET
    path('citas/crear/', CrearCitaAPIView.as_view()),        # POST

    # 🔍 DETALLE / EDITAR
    path('citas/<int:pk>/', DetalleMiCitaAPIView.as_view()), # GET / PUT / PATCH

    # 🗑 ELIMINAR
    path('citas/<int:pk>/eliminar/', EliminarCitaAPIView.as_view()),

    # 📊 DISPONIBILIDAD
    path('citas/disponibilidad/', HorariosDisponiblesAPIView.as_view()),

    # 🏢 EMPRESA
    path('empresa/citas/', CitasEmpresaAPIView.as_view()),

    # 🔄 CAMBIAR ESTADO
    path('citas/<int:pk>/estado/', CambiarEstadoCitaAPIView.as_view()),
    # 📅 AGENDAS
    path('agendas/<int:establecimiento_id>/', obtener_agendas),

    # ⭐ CALIFICACIONES
    path('calificaciones/crear/', CrearCalificacionAPIView.as_view()),
    path('calificaciones/establecimiento/<int:establecimiento_id>/', CalificacionesEstablecimientoAPIView.as_view()),
    path('resenas/crear/', CrearResenaAPIView.as_view()),
    path('resenas/mis/', MisResenasAPIView.as_view()),

    # 📊 DASHBOARD
    path('dashboard/empresa/', DashboardEmpresaAPIView.as_view()),

    # 🔔 NOTIFICACIONES
    path('notificaciones/', MisNotificacionesAPIView.as_view()),
    path('notificaciones/<int:pk>/leida/', MarcarLeidaAPIView.as_view()),
    
    
      # =========================
    # 🔐 ADMIN
    # =========================

    path('admin/usuarios/', UsuarioListCreateView.as_view()),
    path('admin/usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view()),

    
    path('admin/vehiculos/<str:placa>/', VehiculoRetrieveUpdateDestroyView.as_view()),

    path('admin/servicios/', ServicioListCreateView.as_view()),
    path('admin/servicios/<int:pk>/', ServicioRetrieveUpdateDestroyView.as_view()),

    path('admin/prestaciones/', PrestacionListCreateView.as_view()),
    path('admin/prestaciones/<int:pk>/', PrestacionRetrieveUpdateDestroyView.as_view()),

    path('admin/calificaciones/', CalificacionListCreateView.as_view()),
    path('admin/calificaciones/<int:pk>/', CalificacionRetrieveUpdateDestroyView.as_view()),

    path('admin/notificaciones/', NotificacionListCreateView.as_view()),
    path('admin/notificaciones/<int:pk>/', NotificacionRetrieveUpdateDestroyView.as_view()),
    path('horarios-disponibles/', horarios_disponibles),
]
