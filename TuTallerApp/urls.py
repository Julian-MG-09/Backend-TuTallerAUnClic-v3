from django.urls import path
from .views import (
    RegistroView, LoginView, PerfilView,
    VehiculoCreateView, MisVehiculosView,
    VehiculoListCreateView, VehiculoRetrieveUpdateDestroyView,
    EstablecimientoListView, EstablecimientoDetailView,
    EstablecimientoCreateView, EstablecimientoUpdateDestroyView,
    ServiciosPorEstablecimientoView, ServicioCreateView,
    ServicioListView, ServicioRetrieveUpdateDestroyView,
    CrearCitaView, MisCitasView, DetalleMiCitaView,
    CitasEmpresaView, CambiarEstadoCitaView,
    PrestacionListCreateView, PrestacionRetrieveUpdateDestroyView,
    DashboardEmpresaView,
    CrearCalificacionView, CalificacionesEstablecimientoView,
    CalificacionListCreateView, CalificacionRetrieveUpdateDestroyView,
    MisNotificacionesView, MarcarLeidaView,
    NotificacionListCreateView, NotificacionRetrieveUpdateDestroyView,
    UsuarioListCreateView, UsuarioRetrieveUpdateDestroyView,
    RolListView, RolListCreateView, RolRetrieveUpdateDestroyView,
    TipoEstablecimientoListView, TipoServicioListView,
    AgendaListCreateView,
    home, login_web,
    TipoEstablecimientoListCreateView, TipoEstablecimientoRetrieveUpdateDestroyView,
    TipoServicioListCreateView, TipoServicioRetrieveUpdateDestroyView,
    ServicioListCreateView, AgendaRetrieveUpdateDestroyView
)
from .views import AdminDashboardView
from .views import PerfilUpdateView
from .views import AnuncioListView, AnuncioAdminViewSet, AnuncioAdminDetailView, StatsPublicasView


urlpatterns = [
    path('', home),
    path('login/', login_web, name='login_web'),

    # Auth
    path('usuarios/register/',          RegistroView.as_view()),
    path('usuarios/login/',             LoginView.as_view()),
    path('usuarios/perfil/',            PerfilView.as_view()),

    # Vehiculos usuario
    path('usuarios/vehiculos/',         MisVehiculosView.as_view()),
    path('usuarios/vehiculos/crear/',   VehiculoCreateView.as_view()),

    # Establecimientos publicos
    path('establecimientos/',           EstablecimientoListView.as_view()),
    path('establecimientos/<int:pk>/',  EstablecimientoDetailView.as_view()),
    path('establecimientos/crear/',     EstablecimientoCreateView.as_view()),

    # Servicios publicos
    path('servicios/',                  ServicioListView.as_view()),
    path('servicios/establecimiento/<int:establecimiento_id>/', ServiciosPorEstablecimientoView.as_view()),
    path('api/admin/servicios/',          ServicioListCreateView.as_view()),

    # Citas
    path('citas/crear/',                CrearCitaView.as_view()),
    path('citas/mis-citas/',            MisCitasView.as_view()),
    path('citas/<int:pk>/',             DetalleMiCitaView.as_view()),
    path('citas/empresa/<int:establecimiento_id>/', CitasEmpresaView.as_view()),
    path('citas/<int:pk>/estado/',      CambiarEstadoCitaView.as_view()),
    path('citas/dashboard/<int:establecimiento_id>/', DashboardEmpresaView.as_view()),

    # Calificaciones publicas
    path('calificaciones/crear/',       CrearCalificacionView.as_view()),
    path('calificaciones/establecimiento/<int:establecimiento_id>/', CalificacionesEstablecimientoView.as_view()),

    # Notificaciones usuario
    path('notificaciones/',             MisNotificacionesView.as_view()),
    path('notificaciones/<int:pk>/leida/', MarcarLeidaView.as_view()),

    # Roles publicos (para registro)
    path('roles/',                      RolListView.as_view()),

    # Tipos publicos
    path('tipos-establecimiento/',      TipoEstablecimientoListView.as_view()),
    path('tipos-servicio/',             TipoServicioListView.as_view()),

    # ==========================================
    # RUTAS ADMIN
    # ==========================================
    path('api/admin/usuarios/',              UsuarioListCreateView.as_view()),
    path('api/admin/usuarios/<int:pk>/',     UsuarioRetrieveUpdateDestroyView.as_view()),

    path('api/admin/vehiculos/',             VehiculoListCreateView.as_view()),
    path('api/admin/vehiculos/<str:placa>/', VehiculoRetrieveUpdateDestroyView.as_view()),

    path('api/admin/establecimientos/<int:pk>/', EstablecimientoUpdateDestroyView.as_view()),

    path('api/admin/servicios/<int:pk>/',    ServicioRetrieveUpdateDestroyView.as_view()),

    path('api/admin/prestaciones/',          PrestacionListCreateView.as_view()),
    path('api/admin/prestaciones/<int:pk>/', PrestacionRetrieveUpdateDestroyView.as_view()),

    path('api/admin/calificaciones/',        CalificacionListCreateView.as_view()),
    path('api/admin/calificaciones/<int:pk>/', CalificacionRetrieveUpdateDestroyView.as_view()),

    path('api/admin/notificaciones/',        NotificacionListCreateView.as_view()),
    path('api/admin/notificaciones/<int:pk>/', NotificacionRetrieveUpdateDestroyView.as_view()),

    path('api/admin/roles/',                 RolListCreateView.as_view()),
    path('api/admin/roles/<int:pk>/',        RolRetrieveUpdateDestroyView.as_view()),

    path('api/admin/agenda/',                AgendaListCreateView.as_view()),
    path('api/admin/agenda/<int:pk>/', AgendaRetrieveUpdateDestroyView.as_view()),

    path('api/admin/tipos-establecimiento/',          TipoEstablecimientoListCreateView.as_view()),
    path('api/admin/tipos-establecimiento/<int:pk>/', TipoEstablecimientoRetrieveUpdateDestroyView.as_view()),
    path('api/admin/tipos-servicio/',                 TipoServicioListCreateView.as_view()),
    path('api/admin/tipos-servicio/<int:pk>/',        TipoServicioRetrieveUpdateDestroyView.as_view()),

    path('api/admin/dashboard/', AdminDashboardView.as_view()),

    path('usuarios/perfil/update/', PerfilUpdateView.as_view()),


    # Publica
    path('anuncios/', AnuncioListView.as_view()),
    
    # Admin
    path('api/admin/anuncios/',      AnuncioAdminViewSet.as_view()),
    path('api/admin/anuncios/<pk>/', AnuncioAdminDetailView.as_view()),

    path('stats/', StatsPublicasView.as_view()),
]


