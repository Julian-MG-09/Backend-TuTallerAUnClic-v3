from django.contrib import admin
from .models import (
    Rol, Usuario, TipoEstablecimiento, Establecimiento,
    TipoServicio, Servicio, Vehiculo, Agenda,
    PrestacionServicio, Calificacion, Notificacion
)


# ============================
# USUARIOS
# ============================

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined',)


# ============================
# ESTABLECIMIENTOS
# ============================

@admin.register(TipoEstablecimiento)
class TipoEstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'telefono', 'propietario')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'direccion')
    autocomplete_fields = ('propietario',)


# ============================
# SERVICIOS
# ============================

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'establecimiento', 'tipo_servicio')
    list_filter = ('tipo_servicio',)
    search_fields = ('nombre',)  # 🔥 ESTA LÍNEA ES LA CLAVE
    autocomplete_fields = ('establecimiento',)

# ============================
# VEHÍCULOS
# ============================

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'usuario')
    search_fields = ('placa',)
    autocomplete_fields = ('usuario',)


# ============================
# CITAS
# ============================

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora')
    list_filter = ('fecha',)


@admin.register(PrestacionServicio)
class PrestacionServicioAdmin(admin.ModelAdmin):
    list_display = (
        'establecimiento', 'usuario', 'vehiculo',
        'servicio', 'fecha', 'estado'
    )
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'establecimiento__nombre')
    autocomplete_fields = ('usuario', 'establecimiento', 'vehiculo', 'servicio')


# ============================
# CALIFICACIONES
# ============================

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('prestacion', 'puntuacion', 'fecha')
    list_filter = ('puntuacion',)
    search_fields = ('prestacion__usuario__username',)


# ============================
# NOTIFICACIONES
# ============================

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'leida', 'fecha')
    list_filter = ('leida',)
    search_fields = ('usuario__username', 'titulo')