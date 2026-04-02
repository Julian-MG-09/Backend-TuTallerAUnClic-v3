from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .serializers import CitaSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView


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

    fecha = request.GET.get('fecha')

    agendas = Agenda.objects.filter(
        establecimiento_id=establecimiento_id
    )

    ocupadas = PrestacionServicio.objects.filter(
        establecimiento_id=establecimiento_id,
        fecha=fecha,
        estado__in=['pendiente', 'confirmada']
    ).values_list('agenda_id', flat=True)

    disponibles = agendas.exclude(id__in=ocupadas)

    data = [
        {
            "id": a.id,
            "hora": a.hora.strftime("%H:%M")
        }
        for a in disponibles
    ]

    return Response(data)



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