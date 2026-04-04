from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .serializers import CitaSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, timedelta, time

from .models import (
    PrestacionServicio,
    Agenda ,
    Establecimiento,
    Servicio,
    Calificacion,Cita,Establecimiento, Servicio
)

from .serializers import (
    UsuarioSerializer,
    CitaSerializer,
    EstablecimientoSerializer,
    ServicioSerializer,
    CalificacionSerializer
)


def home(request):
    return render(request, "home.html")


def login_web(request):
    return render(request, "login.html")


@login_required
def mis_citas_web(request):
    citas = PrestacionServicio.objects.filter(usuario=request.user)
    return render(request, "mis_citas.html", {"citas": citas})



class UsuarioMeView(UpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    


class CrearCitaView(CreateAPIView):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        print("📥 DATA:", request.data)

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("🔥 ERROR REAL:", serializer.errors)
            return Response(serializer.errors, status=400)

        self.perform_create(serializer)

        return Response(serializer.data, status=201)
    
    
    
    




@api_view(['GET'])
def obtener_agendas(request, establecimiento_id):

    fecha_str = request.GET.get("fecha")

    if not fecha_str:
        return Response({"error": "Fecha requerida"}, status=400)

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

    # 🕒 HORARIO BASE (8am a 6pm cada hora)
    hora_inicio = time(8, 0)
    hora_fin = time(18, 0)

    horas = []
    actual = datetime.combine(fecha, hora_inicio)

    while actual.time() <= hora_fin:
        horas.append(actual.time())
        actual += timedelta(hours=1)

    # 🚫 HORAS OCUPADAS (citas ya creadas)
    ocupadas = Agenda.objects.filter(fecha=fecha).values_list("hora", flat=True)

    # ✅ DISPONIBLES
    disponibles = [h for h in horas if h not in ocupadas]

    # 🎯 RESPUESTA
    data = [
        {
            "id": i + 1,
            "hora": h.strftime("%H:%M")
        }
        for i, h in enumerate(disponibles)
    ]

    return Response(data)



# views.py


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def horarios_disponibles(request):
    establecimiento_id = request.GET.get('establecimiento')
    fecha = request.GET.get('fecha')

    establecimiento = Establecimiento.objects.get(id=establecimiento_id)

    # 🔥 Generar horas dinámicamente
    hora_inicio = establecimiento.hora_apertura
    hora_fin = establecimiento.hora_cierre

    horas = []
    actual = datetime.combine(datetime.today(), hora_inicio)
    fin = datetime.combine(datetime.today(), hora_fin)

    while actual <= fin:
        horas.append(actual.strftime("%H:%M"))
        actual += timedelta(hours=1)

    # 🔥 Obtener citas ocupadas
    ocupadas = Cita.objects.filter(
        establecimiento_id=establecimiento_id,
        fecha=fecha
    ).values_list('hora', flat=True)

    ocupadas = [h.strftime("%H:%M") for h in ocupadas]

    # 🔥 Filtrar disponibles
    disponibles = [h for h in horas if h not in ocupadas]

    return Response(disponibles)


class MisCitasView(ListAPIView):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cita.objects.filter(usuario=self.request.user)
    
    
    

class EstablecimientosView(ListAPIView):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer


class ServiciosPorEstablecimiento(ListAPIView):
    serializer_class = ServicioSerializer

    def get_queryset(self):
        establecimiento_id = self.kwargs['id']
        return Servicio.objects.filter(establecimiento_id=establecimiento_id)
    
    
    
    

class CrearCalificacionView(CreateAPIView):
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)