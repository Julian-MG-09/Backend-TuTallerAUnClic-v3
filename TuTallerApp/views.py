from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny
from .models import Rol
from .serializers import RolSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from rest_framework import status

class RolListView(generics.ListAPIView):
    queryset = Rol.objects.filter(activo=True)
    serializer_class = RolSerializer
    permission_classes = [AllowAny]

from .models import (
    Usuario,
    Establecimiento,
    PrestacionServicio,
    Vehiculo,
    Calificacion,
    Notificacion,
    Servicio
)

from .serializers import (
    UsuarioSerializer,
    EstablecimientoSerializer,
    PrestacionServicioSerializer,
    VehiculoSerializer,
    CalificacionSerializer,
    NotificacionSerializer,
    ServicioSerializer
)

from .permissions import EsCliente, EsEmpresa, EsAdmin

from django.db.models import Q, Count, Avg


# ==============================
# 🔐 AUTENTICACIÓN
# ==============================

class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UsuarioSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)



class LoginView(TokenObtainPairView):
    pass


class PerfilView(generics.RetrieveAPIView):
    serializer_class   = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# ==============================
# 🏢 ESTABLECIMIENTOS
# ==============================

class EstablecimientoListView(generics.ListAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class EstablecimientoDetailView(generics.RetrieveAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class EstablecimientoCreateView(generics.CreateAPIView):
    serializer_class = EstablecimientoSerializer
    permission_classes = [EsAdmin]


# ==============================
# 🛠 SERVICIOS
# ==============================

class ServiciosPorEstablecimientoView(generics.ListAPIView):
    serializer_class = ServicioSerializer

    def get_queryset(self):
        return Servicio.objects.filter(
            establecimiento_id=self.kwargs['establecimiento_id']
        )


class ServicioCreateView(generics.CreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]


# ==============================
# 🚗 VEHÍCULOS
# ==============================

class VehiculoCreateView(generics.CreateAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MisVehiculosView(generics.ListAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehiculo.objects.filter(usuario=self.request.user)


# ==============================
# 📅 CITAS
# ==============================

class CrearCitaView(generics.CreateAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsCliente]

    def perform_create(self, serializer):

        establecimiento = serializer.validated_data['establecimiento']
        agenda = serializer.validated_data['agenda']
        fecha = serializer.validated_data['fecha']

        # Validar horario
        if not (establecimiento.hora_apertura <= agenda.hora <= establecimiento.hora_cierre):
            raise ValidationError("Horario fuera del rango permitido.")

        # Evitar doble reserva
        existe = PrestacionServicio.objects.filter(
            establecimiento=establecimiento,
            fecha=fecha,
            agenda=agenda,
            estado__in=['pendiente', 'confirmada']
        ).exists()

        if existe:
            raise ValidationError("Ese horario ya está reservado.")

        cita = serializer.save(usuario=self.request.user, estado='pendiente')

        # Notificar empresa
        Notificacion.objects.create(
            usuario=cita.establecimiento.propietario,
            titulo="Nueva cita",
            mensaje=f"Tienes una nueva cita para el {cita.fecha}"
        )


class MisCitasView(generics.ListAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(usuario=self.request.user)


class DetalleMiCitaView(generics.RetrieveAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsCliente]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(usuario=self.request.user)


class CitasEmpresaView(generics.ListAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsEmpresa]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(
            establecimiento__propietario=self.request.user
        )


class CambiarEstadoCitaView(APIView):
    permission_classes = [EsEmpresa]

    def patch(self, request, pk):

        try:
            cita = PrestacionServicio.objects.get(
                pk=pk,
                establecimiento__propietario=request.user
            )
        except PrestacionServicio.DoesNotExist:
            raise ValidationError("No tienes permiso para modificar esta cita.")

        nuevo_estado = request.data.get("estado")

        estados_validos = [
            e[0] for e in PrestacionServicio._meta.get_field('estado').choices
        ]

        if nuevo_estado not in estados_validos:
            raise ValidationError("Estado inválido.")

        cita.estado = nuevo_estado
        cita.save()

        # Notificar cliente
        Notificacion.objects.create(
            usuario=cita.usuario,
            titulo="Estado actualizado",
            mensaje=f"Tu cita fue {cita.estado}"
        )

        return Response({"mensaje": "Estado actualizado correctamente"})


# ==============================
# ⭐ CALIFICACIONES
# ==============================

class CrearCalificacionView(generics.CreateAPIView):
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]


class CalificacionesEstablecimientoView(generics.ListAPIView):
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        return Calificacion.objects.filter(
            prestacion__establecimiento_id=self.kwargs['establecimiento_id']
        )


# ==============================
# 📊 DASHBOARD
# ==============================

class DashboardEmpresaView(APIView):
    permission_classes = [EsEmpresa]

    def get(self, request, establecimiento_id):

        total_citas = PrestacionServicio.objects.filter(
            establecimiento_id=establecimiento_id,
            establecimiento__propietario=request.user
        ).count()

        pendientes = PrestacionServicio.objects.filter(
            establecimiento_id=establecimiento_id,
            establecimiento__propietario=request.user,
            estado='pendiente'
        ).count()

        return Response({
            "total_citas": total_citas,
            "pendientes": pendientes
        })


# ==============================
# 🔔 NOTIFICACIONES
# ==============================

class MisNotificacionesView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha')


class MarcarLeidaView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        notificacion = Notificacion.objects.get(
            pk=pk,
            usuario=request.user
        )

        notificacion.leida = True
        notificacion.save()

        return Response({"mensaje": "Notificación marcada como leída"})
    
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")


def login_web(request):
    return render(request, "login.html")


@login_required
def mis_citas_web(request):
    citas = PrestacionServicio.objects.filter(usuario=request.user)
    return render(request, "mis_citas.html", {"citas": citas})



from rest_framework.permissions import AllowAny
from .models import Rol, Agenda, TipoEstablecimiento, TipoServicio
from .serializers import (
    RolSerializer, AgendaSerializer,
    TipoEstablecimientoSerializer, TipoServicioSerializer,
    NotificacionSerializer
)

# USUARIOS
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdmin]

class UsuarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdmin]

# ESTABLECIMIENTOS
class EstablecimientoUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer
    permission_classes = [EsAdmin]

# SERVICIOS
class ServicioListCreateView(generics.ListCreateAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [EsAdmin]

class ServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [EsAdmin]

class ServicioListView(generics.ListAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [EsAdmin]

# PRESTACIONES
class PrestacionListCreateView(generics.ListCreateAPIView):
    queryset = PrestacionServicio.objects.all()
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsAdmin]

class PrestacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrestacionServicio.objects.all()
    serializer_class = PrestacionServicioSerializer
    permission_classes = [EsAdmin]

# CALIFICACIONES
class CalificacionListCreateView(generics.ListCreateAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [EsAdmin]

class CalificacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [EsAdmin]

# NOTIFICACIONES
class NotificacionListCreateView(generics.ListCreateAPIView):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [EsAdmin]

class NotificacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [EsAdmin]

# VEHICULOS
class VehiculoListCreateView(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [EsAdmin]

class VehiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [EsAdmin]
    lookup_field = 'placa'

# ROLES
class RolListView(generics.ListAPIView):
    queryset = Rol.objects.filter(activo=True)
    serializer_class = RolSerializer
    permission_classes = [AllowAny]

class RolListCreateView(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [EsAdmin]

class RolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [EsAdmin]

# TIPOS
class TipoEstablecimientoListView(generics.ListAPIView):
    queryset = TipoEstablecimiento.objects.all()
    serializer_class = TipoEstablecimientoSerializer
    permission_classes = [AllowAny]

class TipoServicioListView(generics.ListAPIView):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [AllowAny]

# AGENDA
class AgendaListCreateView(generics.ListCreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [EsAdmin]

class AgendaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [EsAdmin]

class TipoEstablecimientoListCreateView(generics.ListCreateAPIView):
    queryset = TipoEstablecimiento.objects.all()
    serializer_class = TipoEstablecimientoSerializer
    permission_classes = [EsAdmin]

class TipoEstablecimientoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoEstablecimiento.objects.all()
    serializer_class = TipoEstablecimientoSerializer
    permission_classes = [EsAdmin]

class TipoServicioListCreateView(generics.ListCreateAPIView):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [EsAdmin]

class TipoServicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [EsAdmin]


from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView

class AdminDashboardView(APIView):
    permission_classes = [EsAdmin]

    def get(self, request):
        hoy = timezone.now().date()
        hace_6_meses = hoy - timedelta(days=180)

        # Conteos generales
        total_usuarios       = Usuario.objects.count()
        total_establecimientos = Establecimiento.objects.count()
        total_servicios      = Servicio.objects.count()
        total_vehiculos      = Vehiculo.objects.count()
        total_prestaciones   = PrestacionServicio.objects.count()
        total_calificaciones = Calificacion.objects.count()

        # Usuarios por rol
        usuarios_por_rol = list(
            Usuario.objects.values('rol__nombre')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # Prestaciones por estado
        prestaciones_por_estado = list(
            PrestacionServicio.objects.values('estado')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # Prestaciones por mes (ultimos 6 meses)
        prestaciones_por_mes = []
        for i in range(5, -1, -1):
            fecha = hoy - timedelta(days=30 * i)
            count = PrestacionServicio.objects.filter(
                fecha__year=fecha.year,
                fecha__month=fecha.month
            ).count()
            prestaciones_por_mes.append({
                'mes': fecha.strftime('%b %Y'),
                'total': count
            })

        # Top establecimientos por calificacion
        top_establecimientos = list(
            Establecimiento.objects.annotate(
                promedio=Avg('prestacionservicio__calificacion__puntuacion'),
                total_citas=Count('prestacionservicio')
            ).filter(promedio__isnull=False)
            .order_by('-promedio')[:5]
            .values('id', 'nombre', 'promedio', 'total_citas')
        )

        # Calificacion promedio general
        cal_promedio = Calificacion.objects.aggregate(promedio=Avg('puntuacion'))['promedio']

        # Ultimas 5 prestaciones
        ultimas_prestaciones = list(
            PrestacionServicio.objects.select_related(
                'usuario', 'establecimiento', 'servicio'
            ).order_by('-fecha', '-id')[:5]
            .values(
                'id', 'fecha', 'estado',
                'usuario__username',
                'establecimiento__nombre',
                'servicio__nombre'
            )
        )

        # Notificaciones no leidas
        notificaciones_no_leidas = Notificacion.objects.filter(leida=False).count()

        # Nuevos usuarios este mes
        nuevos_este_mes = Usuario.objects.filter(
            date_joined__year=hoy.year,
            date_joined__month=hoy.month
        ).count()

        return Response({
            'resumen': {
                'total_usuarios':         total_usuarios,
                'total_establecimientos': total_establecimientos,
                'total_servicios':        total_servicios,
                'total_vehiculos':        total_vehiculos,
                'total_prestaciones':     total_prestaciones,
                'total_calificaciones':   total_calificaciones,
                'calificacion_promedio':  round(cal_promedio, 1) if cal_promedio else 0,
                'notificaciones_no_leidas': notificaciones_no_leidas,
                'nuevos_este_mes':        nuevos_este_mes,
            },
            'usuarios_por_rol':         usuarios_por_rol,
            'prestaciones_por_estado':  prestaciones_por_estado,
            'prestaciones_por_mes':     prestaciones_por_mes,
            'top_establecimientos':     top_establecimientos,
            'ultimas_prestaciones':     ultimas_prestaciones,
        })


class PerfilUpdateView(generics.UpdateAPIView):
    serializer_class   = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

from django.utils import timezone
from .models import Anuncio
from .serializers import AnuncioSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Publica — solo anuncios activos y vigentes
class AnuncioListView(generics.ListAPIView):
    serializer_class   = AnuncioSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hoy = timezone.now().date()
        return Anuncio.objects.filter(
            activo=True
        ).filter(
            Q(fecha_inicio__isnull=True) | Q(fecha_inicio__lte=hoy)
        ).filter(
            Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=hoy)
        )

    def get_serializer_context(self):
        return {'request': self.request}

# Admin — CRUD completo
class AnuncioAdminViewSet(generics.ListCreateAPIView):
    serializer_class   = AnuncioSerializer
    permission_classes = [EsAdmin]
    parser_classes     = [MultiPartParser, FormParser]
    queryset           = Anuncio.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

class AnuncioAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = AnuncioSerializer
    permission_classes = [EsAdmin]
    parser_classes     = [MultiPartParser, FormParser]
    queryset           = Anuncio.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class StatsPublicasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from django.db.models import Avg
        return Response({
            'total_establecimientos': Establecimiento.objects.count(),
            'total_usuarios':         Usuario.objects.count(),
            'total_prestaciones':     PrestacionServicio.objects.count(),
            'calificacion_promedio':  round(
                Calificacion.objects.aggregate(p=Avg('puntuacion'))['p'] or 0, 1
            ),
        })