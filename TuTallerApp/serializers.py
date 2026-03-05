from rest_framework import serializers
from .models import Establecimiento,PrestacionServicio,Servicio,Calificacion,Usuario, Vehiculo

from .models import Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(write_only=True)
    rol_nombre  = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model  = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'rol', 'rol_nombre', 'password',
            'is_active', 'date_joined'
        ]

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username   = validated_data['username'],
            email      = validated_data.get('email', ''),
            password   = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name  = validated_data.get('last_name', ''),
            telefono   = validated_data.get('telefono', ''),
            rol        = validated_data.get('rol'),
        )
        return user


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'



# servicios/serializers.py


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
#citas/serializers.py

class PrestacionServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestacionServicio
        fields = '__all__'

# calificaciones/serializers.py

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'
        
        


from rest_framework import serializers
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

from .models import Rol, Agenda, TipoEstablecimiento, TipoServicio

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion', 'fecha_actualizacion']

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

class TipoEstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEstablecimiento
        fields = '__all__'

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = '__all__'