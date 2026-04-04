from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone




from .models import (
    Usuario,
    Establecimiento,Cita,
    Servicio,
    Vehiculo,
    PrestacionServicio,
    Calificacion,
    Notificacion
)

from .serializers import (CitaSerializer,
    UsuarioSerializer,
    EstablecimientoSerializer,
    ServicioSerializer,
    VehiculoSerializer,
    PrestacionServicioSerializer,
    CalificacionSerializer,
    NotificacionSerializer
)

from .permissions import EsCliente, EsEmpresa


# =====================================
# 🏢 ESTABLECIMIENTOS
# =====================================


class EstablecimientosRecomendadosAPIView(APIView):

    def get(self, request):

        user = request.user

        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        establecimientos = Establecimiento.objects.annotate(
            promedio=Avg('prestacionservicio__calificacion__puntuacion'),
            total=Count('prestacionservicio')
        )

        establecimientos = list(establecimientos)

        # =========================
        # 📍 DISTANCIA
        # =========================
        if lat and lng:
            lat = float(lat)
            lng = float(lng)

            for est in establecimientos:
                est.distancia = calcular_distancia(
                    lat, lng,
                    float(est.latitud),
                    float(est.longitud)
                )
        else:
            for est in establecimientos:
                est.distancia = 9999

        # =========================
        # 🧠 HISTORIAL DEL USUARIO
        # =========================
        historial = PrestacionServicio.objects.filter(
            usuario=user
        ).values_list('establecimiento_id', flat=True)

        # =========================
        # 🧠 SCORE INTELIGENTE
        # =========================
        for est in establecimientos:

            score = 0

            # Cercanía
            score += max(0, 10 - est.distancia)

            # Calificación
            score += (est.promedio or 0) * 2

            # Popularidad
            score += (est.total or 0) * 0.1

            # Si ya lo usó → boost
            if est.id in historial:
                score += 5

            est.score = score

        # =========================
        # 🔥 ORDEN FINAL
        # =========================
        establecimientos.sort(
            key=lambda x: x.score,
            reverse=True
        )

        serializer = EstablecimientoSerializer(
            establecimientos,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)



class EstablecimientoListAPIView(generics.ListAPIView):
    serializer_class = EstablecimientoSerializer

    def get_queryset(self):
        return Establecimiento.objects.annotate(
            promedio=Avg('prestacionservicio__calificacion__puntuacion'),
            total=Count('prestacionservicio__calificacion')
        )

    def list(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())

        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        # =========================
        # 📍 CALCULAR DISTANCIA
        # =========================
        if lat and lng:
            lat = float(lat)
            lng = float(lng)

            for est in queryset:
                est.distancia = calcular_distancia(
                    lat, lng,
                    float(est.latitud),
                    float(est.longitud)
                )
        else:
            for est in queryset:
                est.distancia = 9999  # lejos por defecto

        # =========================
        # 🧠 ORDEN INTELIGENTE
        # =========================
        queryset.sort(
            key=lambda x: (
                x.distancia,                # más cercano primero
                -(x.promedio or 0),         # mejor calificado
                -(x.total or 0)             # más popular
            )
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
        # =========================
        # 🔥 SOLO CON DISPONIBILIDAD
        # =========================
        disponible = self.request.query_params.get('disponible')
        if disponible == 'true':
            queryset = queryset.filter(
                prestacionservicio__estado='pendiente'
            ).distinct()

        return queryset.order_by('-promedio', '-total')


class EstablecimientoDetailAPIView(generics.RetrieveAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer

class EstablecimientoCreateAPIView(generics.CreateAPIView):
    serializer_class = EstablecimientoSerializer
    permission_classes = [EsEmpresa]

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)
        
        


class TopEstablecimientosAPIView(generics.ListAPIView):
    serializer_class = EstablecimientoSerializer

    def get_queryset(self):
        return Establecimiento.objects.annotate(
            promedio=Avg('prestacionservicio__calificacion__puntuacion'),
            total=Count('prestacionservicio__calificacion')
        ).filter(
            promedio__isnull=False
        ).order_by('-promedio', '-total')[:10]


# =====================================
# 🛠 SERVICIOS
# =====================================

class ServiciosPorEstablecimientoAPIView(generics.ListAPIView):
    serializer_class = ServicioSerializer

    def get_queryset(self):
        return Servicio.objects.filter(
            establecimiento_id=self.kwargs['establecimiento_id']
        )


class ServicioCreateAPIView(generics.CreateAPIView):
    serializer_class = ServicioSerializer
    permission_classes = [EsEmpresa]

    def perform_create(self, serializer):
        establecimiento = serializer.validated_data['establecimiento']

        if establecimiento.propietario != self.request.user:
            raise ValidationError("No puedes crear servicios en este establecimiento.")

        serializer.save()


# =====================================
# 🚗 VEHÍCULOS
# =====================================

class VehiculoCreateAPIView(generics.CreateAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class MisVehiculosAPIView(generics.ListAPIView):
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vehiculo.objects.filter(usuario=self.request.user)


# =====================================
# 📅 CITAS
# =====================================



class CrearCitaAPIView(generics.CreateAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, EsCliente]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
         
class EditarCitaAPIView(generics.UpdateAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cita.objects.filter(usuario=self.request.user)

    def perform_update(self, serializer):
        cita = self.get_object()

        if cita.estado != 'pendiente':
            raise ValidationError("Solo puedes editar citas pendientes.")

        establecimiento = serializer.validated_data.get('establecimiento', cita.establecimiento)
        fecha = serializer.validated_data.get('fecha', cita.fecha)
        hora = serializer.validated_data.get('hora', cita.hora)

        # 🔥 validar horario
        if not (establecimiento.hora_apertura <= hora <= establecimiento.hora_cierre):
            raise ValidationError("Horario fuera del rango permitido.")

        # 🔥 validar duplicado
        if Cita.objects.filter(
            establecimiento=establecimiento,
            fecha=fecha,
            hora=hora
        ).exclude(pk=cita.pk).exists():
            raise ValidationError("Ese horario ya está reservado.")

        serializer.save()


class MisCitasAPIView(generics.ListAPIView):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cita.objects.filter(usuario=self.request.user)

class DetalleMiCitaAPIView(generics.RetrieveAPIView):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cita.objects.filter(usuario=self.request.user)

class CitasEmpresaAPIView(generics.ListAPIView):
    serializer_class = CitaSerializer
    permission_classes = [EsEmpresa]

    def get_queryset(self):
        return Cita.objects.filter(
            establecimiento__propietario=self.request.user
        )

class CambiarEstadoCitaAPIView(APIView):
    permission_classes = [EsEmpresa]

    def patch(self, request, pk):

        cita = get_object_or_404(
            Cita,
            pk=pk,
            establecimiento__propietario=request.user
        )

        nuevo_estado = request.data.get("estado")

        estados_validos = [
            e[0] for e in Cita._meta.get_field('estado').choices
        ]

        if nuevo_estado not in estados_validos:
            raise ValidationError("Estado inválido.")

        cita.estado = nuevo_estado

        if nuevo_estado == 'finalizada':
            cita.fecha_finalizacion = timezone.now()

        cita.save()

        Notificacion.objects.create(
            usuario=cita.usuario,
            titulo="Estado actualizado",
            mensaje=f"Tu cita fue {cita.estado}"
        )

        return Response({"mensaje": "Estado actualizado correctamente"})    
 
 
 
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from .models import Cita   
    
class EliminarCitaAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 🔐 Seguridad: solo citas del usuario
        return Cita.objects.filter(usuario=self.request.user)

    def perform_destroy(self, instance):
        if instance.estado != 'pendiente':
            raise ValidationError("No puedes eliminar esta cita.")
        instance.delete()

    # 🔥 Opcional PRO: mensajes más claros
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # aquí ya filtra por usuario
            self.perform_destroy(instance)
            return Response(
                {"mensaje": "Cita eliminada correctamente"},
                status=status.HTTP_200_OK
            )
        except Cita.DoesNotExist:
            raise NotFound("La cita no existe o no te pertenece")
        except ValidationError as e:
            return Response(
                {"error": str(e.detail[0])},
                status=status.HTTP_400_BAD_REQUEST
            )

# =====================================
# 💬 COMENTARIO EMPRESA
# =====================================

class ComentarioEmpresaAPIView(APIView):
    permission_classes = [EsEmpresa]

    def patch(self, request, pk):

        cita = get_object_or_404(
            PrestacionServicio,
            pk=pk,
            establecimiento__propietario=request.user
        )

        if cita.estado != 'finalizada':
            raise ValidationError("Solo puedes comentar citas finalizadas.")

        comentario = request.data.get("comentario")

        if not comentario:
            raise ValidationError("Debes enviar un comentario.")

        cita.comentario_empresa = comentario
        cita.save()

        return Response({"mensaje": "Comentario agregado correctamente"})


# =====================================
# 🧾 HISTORIAL USUARIO
# =====================================

class HistorialUsuarioAPIView(generics.ListAPIView):
    serializer_class = PrestacionServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrestacionServicio.objects.filter(
            usuario=self.request.user,
            estado='finalizada'
        ).order_by('-fecha_finalizacion')


# =====================================
# ⭐ CALIFICACIONES
# =====================================

class CrearCalificacionAPIView(generics.CreateAPIView):
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        prestacion = serializer.validated_data['prestacion']

        if prestacion.usuario != self.request.user:
            raise ValidationError("No puedes calificar esta cita.")

        if prestacion.estado != 'finalizada':
            raise ValidationError("Solo puedes calificar citas finalizadas.")

        if Calificacion.objects.filter(prestacion=prestacion).exists():
            raise ValidationError("Ya calificaste esta cita.")

        serializer.save()


class CalificacionesEstablecimientoAPIView(generics.ListAPIView):
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        return Calificacion.objects.filter(
            prestacion__establecimiento_id=self.kwargs['establecimiento_id']
        )


# =====================================
# 🔔 NOTIFICACIONES
# =====================================

class MisNotificacionesAPIView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha')


class MarcarLeidaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        notificacion = get_object_or_404(
            Notificacion,
            pk=pk,
            usuario=request.user
        )

        notificacion.leida = True
        notificacion.save()

        return Response({"mensaje": "Notificación marcada como leída"})


# =====================================
# 📊 DASHBOARD EMPRESA
# =====================================

class DashboardEmpresaAPIView(APIView):
    permission_classes = [EsEmpresa]

    def get(self, request):

        total = PrestacionServicio.objects.filter(
            establecimiento__propietario=request.user
        ).count()

        pendientes = PrestacionServicio.objects.filter(
            establecimiento__propietario=request.user,
            estado='pendiente'
        ).count()

        finalizadas = PrestacionServicio.objects.filter(
            establecimiento__propietario=request.user,
            estado='finalizada'
        ).count()

        return Response({
            "total_citas": total,
            "pendientes": pendientes,
            "finalizadas": finalizadas
        })