from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


class Departamento(models.Model):
    """Modelo de Departamentos de la empresa"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    gerente = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='departamento_gerenciado'
    )
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Presupuesto del departamento")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return f"{self.nombre} - Gerente: {self.gerente.get_full_name() if self.gerente else 'Sin asignar'}"

    def clean(self):
        if self.presupuesto < 0:
            raise ValidationError("El presupuesto no puede ser negativo")


class Empleado(models.Model):
    """Modelo de Empleados"""
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('licencia', 'En Licencia'),
        ('despedido', 'Despedido'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')
    numero_empleado = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    puesto = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_contratacion = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.numero_empleado})"

    def clean(self):
        if self.salario < 0:
            raise ValidationError("El salario no puede ser negativo")
        if self.fecha_contratacion > timezone.now().date():
            raise ValidationError("La fecha de contratación no puede ser en el futuro")

    @property
    def antiguedad_meses(self):
        """Calcula la antigüedad en meses"""
        today = timezone.now().date()
        months = (today.year - self.fecha_contratacion.year) * 12
        months += today.month - self.fecha_contratacion.month
        return max(0, months)

    @property
    def dias_trabajados(self):
        """Calcula días trabajados desde la contratación"""
        return (timezone.now().date() - self.fecha_contratacion).days


class Proyecto(models.Model):
    """Modelo de Proyectos"""
    ESTADO_CHOICES = [
        ('planificacion', 'Planificación'),
        ('en_progreso', 'En Progreso'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='proyectos')
    gerente_proyecto = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos_gestionados')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificacion')
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    porcentaje_completado = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    def clean(self):
        if self.presupuesto < 0:
            raise ValidationError("El presupuesto no puede ser negativo")
        if self.fecha_inicio > self.fecha_fin_estimada:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha final")
        if self.porcentaje_completado < 0 or self.porcentaje_completado > 100:
            raise ValidationError("El porcentaje debe estar entre 0 y 100")

    @property
    def dias_para_vencer(self):
        """Calcula días restantes hasta la fecha estimada"""
        if self.estado == 'completado':
            return 0
        delta = self.fecha_fin_estimada - timezone.now().date()
        return max(0, delta.days)

    @property
    def total_horas_registradas(self):
        """Suma total de horas registradas en el proyecto"""
        return self.registrostiempo.aggregate(models.Sum('horas'))['horas__sum'] or 0


class RegistroTiempo(models.Model):
    """Modelo para registros de tiempo de empleados en proyectos"""
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='registrostiempo')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='registrostiempo')
    fecha = models.DateField()
    horas = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField()
    validado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        unique_together = ['empleado', 'proyecto', 'fecha']
        verbose_name_plural = "Registros de Tiempo"

    def __str__(self):
        return f"{self.empleado.user.get_full_name()} - {self.proyecto.nombre} - {self.fecha} ({self.horas}h)"

    def clean(self):
        if self.horas < 0:
            raise ValidationError("Las horas no pueden ser negativas")
        if self.horas > 24:
            raise ValidationError("No se pueden registrar más de 24 horas en un día")
        if self.fecha > timezone.now().date():
            raise ValidationError("No se pueden registrar horas en fechas futuras")

    @property
    def costo_hora(self):
        """Calcula el costo por hora del empleado"""
        if self.empleado.salario and self.horas:
            # Asumiendo 160 horas/mes de trabajo
            return (self.empleado.salario / 160) * self.horas
        return 0
