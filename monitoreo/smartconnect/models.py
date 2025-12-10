from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Departamento(models.Model):
    """Representa un departamento o zona física del sistema."""
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-fecha_creacion']


class Rol(models.Model):
    """Define los roles de usuarios del sistema."""
    OPCIONES_ROL = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    ]
    nombre = models.CharField(max_length=50, choices=OPCIONES_ROL, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class UsuarioSmartConnect(models.Model):
    """Extiende Usuario de Django con roles y departamentos."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='smartconnect_profile')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.rol.nombre})"

    class Meta:
        ordering = ['-fecha_creacion']


class Sensor(models.Model):
    """Representa un sensor RFID (tarjeta o llavero)."""
    ESTADOS_SENSOR = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido'),
    ]
    
    uid_mac = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(3)])
    descripcion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_SENSOR, default='activo')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sensores')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uid_mac} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']


class Barrera(models.Model):
    """Representa una barrera de acceso controlable."""
    ESTADOS_BARRERA = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]
    
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_BARRERA, default='cerrada')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='barreras')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']


class Evento(models.Model):
    """Registra eventos de acceso del sistema."""
    TIPOS_EVENTO = [
        ('acceso_permitido', 'Acceso Permitido'),
        ('acceso_denegado', 'Acceso Denegado'),
        ('evento_manual', 'Evento Manual'),
    ]
    
    tipo = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='eventos')
    barrera = models.ForeignKey(Barrera, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=50, default='procesado')

    def __str__(self):
        return f"{self.tipo} - {self.sensor.uid_mac} - {self.fecha_hora}"

    class Meta:
        ordering = ['-fecha_hora']
