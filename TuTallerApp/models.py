from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# ==============================
# 🔐 ROLES Y USUARIO
# ==============================

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    telefono  = models.CharField(max_length=20, blank=True)
    rol       = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True)
    foto      = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)


# ==============================
# 🏢 ESTABLECIMIENTOS
# ==============================

class TipoEstablecimiento(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Establecimiento(models.Model):
    tipo = models.ForeignKey(TipoEstablecimiento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    descripcion = models.TextField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


# ==============================
# 🛠 SERVICIOS
# ==============================

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# ==============================
# 🚗 VEHÍCULOS
# ==============================

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.placa


# ==============================
# ⏰ AGENDA
# ==============================

from django.conf import settings

class Agenda(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha} - {self.hora}"
    
    
    

class Cita(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey("Establecimiento", on_delete=models.CASCADE)
    servicio = models.ForeignKey("Servicio", on_delete=models.CASCADE)

    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha} {self.hora}"
    
    
# ==============================
# 📅 PRESTACIÓN DE SERVICIO
# ==============================

class PrestacionServicio(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    fecha = models.DateField()
    estado = models.CharField(max_length=30, choices=[
        ('pendiente','Pendiente'),
        ('confirmada','Confirmada'),
        ('cancelada','Cancelada'),
        ('finalizada','Finalizada')
    ])

    class Meta:
        unique_together = ('establecimiento', 'agenda', 'fecha')

    def __str__(self):
        return f"{self.usuario} - {self.estado}"


# ==============================
# ⭐ CALIFICACIONES
# ==============================

class Calificacion(models.Model):
    prestacion = models.ForeignKey(PrestacionServicio, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.puntuacion} estrellas"


# ==============================
# 🔔 NOTIFICACIONES
# ==============================

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"

        

class Anuncio(models.Model):
    TIPO_CHOICES = [
        ('imagen',        'Solo imagen'),
        ('imagen_texto',  'Imagen con texto'),
        ('imagen_boton',  'Imagen con boton'),
    ]

    titulo       = models.CharField(max_length=200, blank=True)
    descripcion  = models.TextField(blank=True)
    imagen       = models.ImageField(upload_to='anuncios/')
    tipo         = models.CharField(max_length=20, choices=TIPO_CHOICES, default='imagen')
    texto_boton  = models.CharField(max_length=50, blank=True)   # ej: "Ver más"
    url_boton    = models.CharField(max_length=500, blank=True)  # ej: /establecimientos/5
    establecimiento = models.ForeignKey(
        'Establecimiento', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='anuncios'
    )
    activo       = models.BooleanField(default=True)
    orden        = models.PositiveIntegerField(default=0)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin    = models.DateField(null=True, blank=True)
    creado_en    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', '-creado_en']

    def __str__(self):
        return self.titulo or f'Anuncio #{self.id}'