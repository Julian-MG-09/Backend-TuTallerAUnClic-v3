from rest_framework import serializers
from .models import Establecimiento,PrestacionServicio,Servicio,Calificacion,Usuario, Vehiculo

from .models import Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    password   = serializers.CharField(write_only=True, required=False)
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    foto_url   = serializers.SerializerMethodField()

    class Meta:
        model  = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'rol', 'rol_nombre',
            'password', 'is_active', 'date_joined',
            'foto', 'foto_url',
        ]

    def get_foto_url(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
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


from .models import Anuncio

class AnuncioSerializer(serializers.ModelSerializer):
    imagen_url      = serializers.SerializerMethodField()
    establecimiento_nombre = serializers.CharField(
        source='establecimiento.nombre', read_only=True
    )

    class Meta:
        model  = Anuncio
        fields = [
            'id', 'titulo', 'descripcion', 'imagen', 'imagen_url',
            'tipo', 'texto_boton', 'url_boton',
            'establecimiento', 'establecimiento_nombre',
            'activo', 'orden', 'fecha_inicio', 'fecha_fin', 'creado_en'
        ]

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return obj.imagen.url if obj.imagen else None