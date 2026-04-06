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
# 🔐 ROL
# =====================================

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']


# =====================================
# 👤 USUARIO (PRO SEGURO)
# =====================================

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    foto_url = serializers.SerializerMethodField()
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'rol_nombre',   # 🔥 solo lectura
            'password',
            'foto',
            'foto_url'
        ]

    # =====================================
    # 📸 FOTO URL COMPLETA
    # =====================================

    def get_foto_url(self, obj):
        request = self.context.get('request')

        if obj.foto and request:
            return request.build_absolute_uri(obj.foto.url)

        return obj.foto.url if obj.foto else None

    # =====================================
    # 🔍 VALIDACIONES
    # =====================================

    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("El usuario ya existe")
        return value

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado")
        return value

    # =====================================
    # 🆕 CREATE (ROL AUTOMÁTICO)
    # =====================================

    def create(self, validated_data):
        password = validated_data.pop('password')

        # 🔥 asignar rol cliente automáticamente
        try:
            rol_cliente = Rol.objects.get(nombre="cliente")
        except Rol.DoesNotExist:
            raise serializers.ValidationError("El rol cliente no existe")

        user = Usuario(**validated_data)
        user.rol = rol_cliente
        user.set_password(password)
        user.save()

        return user

    # =====================================
    # ✏️ UPDATE (SEGURO)
    # =====================================

    def update(self, instance, validated_data):
        # 🔒 evitar cambio de rol desde API
        validated_data.pop('rol', None)

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
        fields = '__all__'
        read_only_fields = ['usuario']  # 🔥 IMPORTANTE

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        # ✅ Tomar datos nuevos o existentes (clave para PATCH)
        establecimiento = data.get('establecimiento') or getattr(instance, 'establecimiento', None)
        fecha = data.get('fecha') or getattr(instance, 'fecha', None)
        hora = data.get('hora') or getattr(instance, 'hora', None)

        # 🚫 Validar que haya datos suficientes
        if not establecimiento or not fecha or not hora:
            raise serializers.ValidationError("Datos incompletos para validar la cita.")

        # 🚫 Evitar citas duplicadas (mismo lugar, fecha y hora)
        query = Cita.objects.filter(
            establecimiento=establecimiento,
            fecha=fecha,
            hora=hora
        )

        # 🔥 Excluir la misma cita si es update
        if instance:
            query = query.exclude(id=instance.id)

        if query.exists():
            raise serializers.ValidationError("Este horario ya está ocupado.")

        return data

    def create(self, validated_data):
        # 🔥 Asignar automáticamente el usuario autenticado
        request = self.context.get('request')
        if request and request.user:
            validated_data['usuario'] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # ✅ Update limpio y seguro
        return super().update(instance, validated_data)

    
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