from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_min_length_3(value):
    """Validar que la cadena tenga mínimo 3 caracteres"""
    if len(value) < 3:
        raise ValidationError('Mínimo 3 caracteres requeridos')

class Departamento(models.Model):
    """Modelo para departamentos o zonas de acceso"""
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_min_length_3]
    )
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class UsuarioRol(models.TextChoices):
    """Definición de roles de usuario"""
    ADMIN = 'admin', 'Administrador'
    OPERADOR = 'operador', 'Operador'


class Sensor(models.Model):
    """Modelo para sensores RFID"""
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido'),
    ]

    uid = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_min_length_3]
    )
    nombre = models.CharField(
        max_length=100,
        validators=[validate_min_length_3]
    )
    tipo = models.CharField(max_length=50, choices=[
        ('tarjeta', 'Tarjeta RFID'),
        ('llavero', 'Llavero RFID'),
        ('otro', 'Otro'),
    ])
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    usuario_asignado = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='sensores'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        unique_together = ['uid', 'departamento']

    def __str__(self):
        return f"{self.nombre} ({self.uid})"

    def clean(self):
        if self.estado not in [choice[0] for choice in self.ESTADO_CHOICES]:
            raise ValidationError({'estado': 'Estado inválido'})


class Barrera(models.Model):
    """Modelo para control de barreras de acceso"""
    nombre = models.CharField(max_length=100)
    departamento = models.OneToOneField(
        Departamento,
        on_delete=models.CASCADE,
        related_name='barrera'
    )
    estado = models.CharField(
        max_length=20,
        choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')],
        default='cerrada'
    )
    modo_manual = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


class Evento(models.Model):
    """Modelo para registrar eventos de acceso"""
    TIPO_EVENTO = [
        ('acceso_intento', 'Intento de Acceso'),
        ('acceso_permitido', 'Acceso Permitido'),
        ('acceso_denegado', 'Acceso Denegado'),
        ('barrera_abierta', 'Barrera Abierta'),
        ('barrera_cerrada', 'Barrera Cerrada'),
    ]

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='eventos'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='eventos'
    )
    tipo = models.CharField(max_length=30, choices=TIPO_EVENTO)
    resultado = models.CharField(
        max_length=20,
        choices=[('permitido', 'Permitido'), ('denegado', 'Denegado')],
        blank=True,
        null=True
    )
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f"{self.tipo} - {self.sensor.nombre} - {self.creado_en}"
