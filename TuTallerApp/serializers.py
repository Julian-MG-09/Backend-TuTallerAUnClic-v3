from django.db.models import Avg
from rest_framework import serializers
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
    Anuncio,
    Cita,
    Resena,
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
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    foto_url = serializers.SerializerMethodField()
    rol_nombre = serializers.SerializerMethodField()

    def get_rol_nombre(self, obj):
        if obj.is_superuser:
            return 'admin'
        return obj.rol.nombre if obj.rol else None

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
            'password2',
            'foto',
            'foto_url'
        ]
        extra_kwargs = {
            'foto': {'required': False, 'allow_null': True},
        }

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
        queryset = Usuario.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("El usuario ya existe.")
        return value

    def validate_email(self, value):
        queryset = Usuario.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("El email ya esta registrado.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if self.instance is None and not password:
            raise serializers.ValidationError({
                'password': "La password es obligatoria."
            })

        if password2 is not None and password != password2:
            raise serializers.ValidationError({
                'password2': "Las contrasenas no coinciden."
            })

        return attrs

    # =====================================
    # 🆕 CREATE (ROL AUTOMÁTICO)
    # =====================================

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('rol', None)

        # 🔥 asignar rol cliente automáticamente
        try:
            rol_cliente = Rol.objects.get(nombre__iexact="cliente")
        except Rol.DoesNotExist:
            raise serializers.ValidationError({
                'rol': "El rol cliente no existe."
            })

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

        # 🔒 ignorar foto si viene null (petición JSON sin archivo)
        if validated_data.get('foto') is None:
            validated_data.pop('foto', None)

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
    tipo_nombre = serializers.CharField(source='tipo.nombre', read_only=True)
    icono_mapa = serializers.SerializerMethodField()

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

    def get_icono_mapa(self, obj):
        tipo = (obj.tipo.nombre or "").strip().lower()
        if 'lav' in tipo:
            return 'lavadero'
        if 'taller' in tipo:
            return 'taller'
        return 'establecimiento'

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
        
        
class CitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cita
        fields = '__all__'
        read_only_fields = ['usuario', 'estado', 'fecha_finalizacion']

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        # ✅ Tomar datos nuevos o existentes (clave para PATCH)
        establecimiento = data.get('establecimiento') or getattr(instance, 'establecimiento', None)
        servicio = data.get('servicio') or getattr(instance, 'servicio', None)
        fecha = data.get('fecha') or getattr(instance, 'fecha', None)
        hora = data.get('hora') or getattr(instance, 'hora', None)

        # 🚫 Validar que haya datos suficientes
        if not establecimiento or not servicio or not fecha or not hora:
            raise serializers.ValidationError("Datos incompletos para validar la cita.")

        if servicio.establecimiento_id != establecimiento.id:
            raise serializers.ValidationError("El servicio no pertenece al establecimiento seleccionado.")

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
        if request and request.user and request.user.is_authenticated:
            validated_data['usuario'] = request.user

        return super().create(validated_data)

    
# =====================================
# 📅 PRESTACIÓN (CITAS)
# =====================================

class PrestacionServicioSerializer(serializers.ModelSerializer):
    comentario_empresa = serializers.CharField(read_only=True)

    class Meta:
        model = PrestacionServicio
        fields = '__all__'





# =====================================
# RESEÑAS
# =====================================

class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = '__all__'
        read_only_fields = ['usuario', 'establecimiento']

    def validate(self, data):
        request = self.context.get('request')
        cita = data.get("cita") or getattr(self.instance, 'cita', None)

        if cita is None:
            raise serializers.ValidationError({"cita": "Debes enviar una cita valida."})

        if request and request.user.is_authenticated and cita.usuario_id != request.user.id:
            raise serializers.ValidationError("No puedes resenar una cita de otro usuario.")

        if cita.estado != "finalizada":
            raise serializers.ValidationError("Solo puedes resenar citas finalizadas.")

        if Resena.objects.filter(cita=cita).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError("Esta cita ya fue resenada.")

        return data




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
