from rest_framework import serializers
from django.db.models import Avg, Count
from .models import (
    Rol,
    Usuario,
    Vehiculo,
    Establecimiento,
    TipoEstablecimiento,
    Servicio,
    TipoServicio,
    PrestacionServicio,
    Calificacion,
    Notificacion,
    Agenda,
    Anuncio
)


# =====================================
# 🧩 ROLES
# =====================================

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'activo']


# =====================================
# 👤 USUARIO
# =====================================

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    foto_url = serializers.SerializerMethodField()
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono',
            'rol', 'rol_nombre',
            'password',
            'foto', 'foto_url'
        ]

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and request:
            return request.build_absolute_uri(obj.foto.url)
        return obj.foto.url if obj.foto else None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Usuario(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =====================================
# 🚗 VEHÍCULOS
# =====================================

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


# =====================================
# 🏢 ESTABLECIMIENTOS
# =====================================

class TipoEstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEstablecimiento
        fields = '__all__'




class EstablecimientoSerializer(serializers.ModelSerializer):
    promedio_calificacion = serializers.SerializerMethodField()
    total_calificaciones = serializers.SerializerMethodField()
    distancia = serializers.SerializerMethodField()

    class Meta:
        model = Establecimiento
        fields = '__all__'

    def get_promedio_calificacion(self, obj):
        promedio = Calificacion.objects.filter(
            prestacion__establecimiento=obj
        ).aggregate(prom=Avg('puntuacion'))['prom']

        return round(promedio, 1) if promedio else 0

    def get_total_calificaciones(self, obj):
        return Calificacion.objects.filter(
            prestacion__establecimiento=obj
        ).count()
        
        
    def get_distancia(self, obj):
         return getattr(obj, 'distancia', None)

# =====================================
# 🛠 SERVICIOS
# =====================================

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


# =====================================
# 📅 AGENDA
# =====================================

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'
        
        
from rest_framework import serializers
from .models import Cita

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ['establecimiento', 'servicio', 'fecha', 'hora', 'descripcion']



class CitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cita
        fields = '__all__'
        read_only_fields = ['usuario']  # 🔥 importante

    def validate(self, data):
        establecimiento = data['establecimiento']
        servicio = data['servicio']
        fecha = data['fecha']
        hora = data['hora']

        # 🔥 1. Validar relación servicio-establecimiento
        if servicio.establecimiento.id != establecimiento.id:
            raise serializers.ValidationError(
                "El servicio no pertenece a este establecimiento"
            )

        # 🔥 2. Validar horario del establecimiento
        if not (establecimiento.hora_apertura <= hora <= establecimiento.hora_cierre):
            raise serializers.ValidationError(
                "La hora está fuera del horario del establecimiento"
            )

        # 🔥 3. Validar cita duplicada
        if Cita.objects.filter(
            establecimiento=establecimiento,
            fecha=fecha,
            hora=hora
        ).exists():
            raise serializers.ValidationError(
                "Ya existe una cita en ese horario"
            )

        return data
    
    
    
# =====================================
# 📅 PRESTACIÓN (CITAS)
# =====================================

class PrestacionServicioSerializer(serializers.ModelSerializer):
    comentario_empresa = serializers.CharField(read_only=True)

    class Meta:
        model = PrestacionServicio
        fields = '__all__'


# =====================================
# ⭐ CALIFICACIONES
# =====================================

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'


# =====================================
# 🔔 NOTIFICACIONES
# =====================================

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'


# =====================================
# 📢 ANUNCIOS
# =====================================

class AnuncioSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    establecimiento_nombre = serializers.CharField(
        source='establecimiento.nombre',
        read_only=True
    )

    class Meta:
        model = Anuncio
        fields = [
            'id', 'titulo', 'descripcion',
            'imagen', 'imagen_url',
            'tipo', 'texto_boton', 'url_boton',
            'establecimiento', 'establecimiento_nombre',
            'activo', 'orden',
            'fecha_inicio', 'fecha_fin',
            'creado_en'
        ]

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return obj.imagen.url if obj.imagen else None