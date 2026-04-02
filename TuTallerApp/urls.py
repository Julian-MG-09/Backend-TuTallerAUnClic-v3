# urls.py (APP)

from django.urls import path



from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (UsuarioMeView,CrearCitaView, 
                    MisCitasView,EstablecimientosView, 
                    ServiciosPorEstablecimiento,
                     CrearCalificacionView)
from .views import obtener_agendas
# AUTH
from .auth_api import (
    RegistroAPIView,login, register,
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
    MisNotificacionesAPIView, EditarCitaAPIView,
    MarcarLeidaAPIView,EliminarCitaAPIView,TopEstablecimientosAPIView
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
    NotificacionRetrieveUpdateDestroyView
)

urlpatterns = [
    
    path('login/', login),
    path('register/', register),
   
    
    # 🔐 AUTH
    path('auth/register/', RegistroAPIView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', RefreshTokenAPIView.as_view()),
    path('auth/logout/', LogoutAPIView.as_view()),
    path('auth/perfil/', PerfilAPIView.as_view()),
    path('auth/cambiar-password/', CambiarPasswordAPIView.as_view()),
    path('auth/perfil/actualizar/', ActualizarPerfilAPIView.as_view()),
    path('auth/eliminar/', EliminarCuentaAPIView.as_view()),

    # 🏢 ESTABLECIMIENTOS
    path('establecimientos/', EstablecimientosView.as_view()),
    path('establecimientos/<int:id>/servicios/', ServiciosPorEstablecimiento.as_view()),
    
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

    # 📅 CITAS
    path('citas/', CrearCitaView.as_view()),
    path('citas/mias/', MisCitasView.as_view()),
    path('citas/crear/', CrearCitaAPIView.as_view()),
    path('citas/mis/', MisCitasAPIView.as_view()),
    path('citas/empresa/', CitasEmpresaAPIView.as_view()),
    path('citas/<int:pk>/estado/', CambiarEstadoCitaAPIView.as_view()),
    # ✏️ editar cita
    path('citas/<int:pk>/editar/', EditarCitaAPIView.as_view()),

    # 🗑 eliminar cita
    path('citas/<int:pk>/eliminar/', EliminarCitaAPIView.as_view()),
    
    path('agendas/<int:establecimiento_id>/', obtener_agendas),


    # ⭐ CALIFICACIONES
    path('calificaciones/', CrearCalificacionView.as_view()),
    
    path('calificaciones/crear/', CrearCalificacionAPIView.as_view()),
    path('calificaciones/establecimiento/<int:establecimiento_id>/', CalificacionesEstablecimientoAPIView.as_view()),

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
]