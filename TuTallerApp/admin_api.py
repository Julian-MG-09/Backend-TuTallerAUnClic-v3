from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    Usuario, Vehiculo, Servicio, PrestacionServicio,
    Calificacion, Notificacion, Rol, Agenda,
    TipoEstablecimiento, TipoServicio, Establecimiento
)

from .serializers import (
    UsuarioSerializer, VehiculoSerializer, ServicioSerializer,
    PrestacionServicioSerializer, CalificacionSerializer,
    NotificacionSerializer, RolSerializer, AgendaSerializer,
    TipoEstablecimientoSerializer, TipoServicioSerializer,
    EstablecimientoSerializer
)

from .permissions import EsAdmin


# ==============================
# 👤 USUARIOS
# ==============================

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 🚗 VEHÍCULOS
# ==============================




class VehiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]
    lookup_field = 'placa'

class VehiculoListCreateView(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]
    
    

# ==============================
# 🏢 ESTABLECIMIENTOS
# ==============================

class EstablecimientoListCreateView(generics.ListCreateAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class EstablecimientoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 🛠 SERVICIOS
# ==============================

class ServicioListCreateView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class ServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 📅 PRESTACIONES (CITAS)
# ==============================

class PrestacionListCreateView(generics.ListCreateAPIView):
    queryset = PrestacionServicio.objects.all()
    serializer_class = PrestacionServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class PrestacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrestacionServicio.objects.all()
    serializer_class = PrestacionServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# ⭐ CALIFICACIONES
# ==============================

class CalificacionListCreateView(generics.ListCreateAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class CalificacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 🔔 NOTIFICACIONES
# ==============================

class NotificacionListCreateView(generics.ListCreateAPIView):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class NotificacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 🧩 ROLES
# ==============================

class RolListCreateView(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class RolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# ⏰ AGENDA
# ==============================

class AgendaListCreateView(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class AgendaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


# ==============================
# 🏷 TIPOS
# ==============================

class TipoEstablecimientoListCreateView(generics.ListCreateAPIView):
    queryset = TipoEstablecimiento.objects.all()
    serializer_class = TipoEstablecimientoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class TipoEstablecimientoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoEstablecimiento.objects.all()
    serializer_class = TipoEstablecimientoSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class TipoServicioListCreateView(generics.ListCreateAPIView):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]


class TipoServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [IsAuthenticated, EsAdmin]