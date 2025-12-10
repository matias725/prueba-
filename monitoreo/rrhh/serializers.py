from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Departamento, Empleado, Proyecto, RegistroTiempo
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuarios de Django"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class DepartamentoSerializer(serializers.ModelSerializer):
    """Serializer para departamentos"""
    gerente_nombre = serializers.CharField(source='gerente.get_full_name', read_only=True)
    total_empleados = serializers.SerializerMethodField()
    total_proyectos = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'gerente', 'gerente_nombre', 'presupuesto', 
                  'activo', 'fecha_creacion', 'total_empleados', 'total_proyectos']
        read_only_fields = ['id', 'fecha_creacion']

    def get_total_empleados(self, obj):
        return obj.empleados.filter(estado='activo').count()

    def get_total_proyectos(self, obj):
        return obj.proyectos.exclude(estado='cancelado').count()

    def validate_presupuesto(self, value):
        if value < 0:
            raise serializers.ValidationError("El presupuesto no puede ser negativo")
        return value


class EmpleadoSerializer(serializers.ModelSerializer):
    """Serializer para empleados"""
    user_info = UserSerializer(source='user', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    antiguedad_meses = serializers.IntegerField(read_only=True)
    dias_trabajados = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['id', 'user', 'user_info', 'full_name', 'numero_empleado', 'departamento', 
                  'departamento_nombre', 'direccion', 'telefono', 'salario', 'puesto', 
                  'estado', 'fecha_contratacion', 'fecha_creacion', 'actualizado',
                  'antiguedad_meses', 'dias_trabajados']
        read_only_fields = ['id', 'fecha_creacion', 'actualizado', 'antiguedad_meses', 'dias_trabajados']

    def validate_salario(self, value):
        if value < 0:
            raise serializers.ValidationError("El salario no puede ser negativo")
        return value

    def validate_numero_empleado(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El número de empleado debe tener al menos 3 caracteres")
        return value

    def validate_fecha_contratacion(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("La fecha de contratación no puede ser en el futuro")
        return value


class EmpleadoDetalleSerializer(EmpleadoSerializer):
    """Serializer detallado para empleado con registros de tiempo"""
    registros_recientes = serializers.SerializerMethodField()
    total_horas_mes = serializers.SerializerMethodField()
    
    def get_registros_recientes(self, obj):
        registros = obj.registrostiempo.all()[:10]
        return RegistroTiempoSerializer(registros, many=True).data

    def get_total_horas_mes(self, obj):
        from django.db.models import Sum
        today = timezone.now().date()
        total = obj.registrostiempo.filter(
            fecha__year=today.year,
            fecha__month=today.month
        ).aggregate(Sum('horas'))['horas__sum'] or 0
        return float(total)


class ProyectoSerializer(serializers.ModelSerializer):
    """Serializer para proyectos"""
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    gerente_nombre = serializers.CharField(source='gerente_proyecto.user.get_full_name', read_only=True)
    dias_para_vencer = serializers.IntegerField(read_only=True)
    total_horas_registradas = serializers.FloatField(read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'departamento', 'departamento_nombre',
                  'gerente_proyecto', 'gerente_nombre', 'estado', 'estado_display',
                  'presupuesto', 'fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real',
                  'porcentaje_completado', 'dias_para_vencer', 'total_horas_registradas',
                  'fecha_creacion', 'actualizado']
        read_only_fields = ['id', 'fecha_creacion', 'actualizado', 'dias_para_vencer', 'total_horas_registradas']

    def validate_presupuesto(self, value):
        if value < 0:
            raise serializers.ValidationError("El presupuesto no puede ser negativo")
        return value

    def validate_porcentaje_completado(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("El porcentaje debe estar entre 0 y 100")
        return value

    def validate(self, data):
        if data['fecha_inicio'] > data['fecha_fin_estimada']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha final")
        return data


class ProyectoDetalleSerializer(ProyectoSerializer):
    """Serializer detallado para proyectos con registros de tiempo"""
    registros_tiempo = serializers.SerializerMethodField()
    empleados_asignados = serializers.SerializerMethodField()
    
    def get_registros_tiempo(self, obj):
        registros = obj.registrostiempo.all()[:20]
        return RegistroTiempoSerializer(registros, many=True).data

    def get_empleados_asignados(self, obj):
        from django.db.models import Sum
        empleados = obj.registrostiempo.values('empleado').distinct()
        empleados_info = []
        for emp_dict in empleados:
            emp = Empleado.objects.get(id=emp_dict['empleado'])
            total_horas = obj.registrostiempo.filter(empleado=emp).aggregate(Sum('horas'))['horas__sum'] or 0
            empleados_info.append({
                'id': emp.id,
                'nombre': emp.user.get_full_name(),
                'total_horas': float(total_horas)
            })
        return empleados_info


class RegistroTiempoSerializer(serializers.ModelSerializer):
    """Serializer para registros de tiempo"""
    empleado_nombre = serializers.CharField(source='empleado.user.get_full_name', read_only=True)
    proyecto_nombre = serializers.CharField(source='proyecto.nombre', read_only=True)
    costo_hora = serializers.FloatField(read_only=True)
    
    class Meta:
        model = RegistroTiempo
        fields = ['id', 'empleado', 'empleado_nombre', 'proyecto', 'proyecto_nombre',
                  'fecha', 'horas', 'descripcion', 'validado', 'costo_hora', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion', 'costo_hora']

    def validate_horas(self, value):
        if value < 0:
            raise serializers.ValidationError("Las horas no pueden ser negativas")
        if value > 24:
            raise serializers.ValidationError("No se pueden registrar más de 24 horas en un día")
        return value

    def validate_fecha(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("No se pueden registrar horas en fechas futuras")
        return value

    def validate(self, data):
        # Validar que el registro sea único por empleado, proyecto y fecha
        if RegistroTiempo.objects.filter(
            empleado=data['empleado'],
            proyecto=data['proyecto'],
            fecha=data['fecha']
        ).exists():
            raise serializers.ValidationError("Ya existe un registro para este empleado, proyecto y fecha")
        return data


class DashboardSerializer(serializers.Serializer):
    """Serializer para el dashboard de estadísticas"""
    total_empleados = serializers.IntegerField()
    total_proyectos = serializers.IntegerField()
    total_horas_registradas = serializers.FloatField()
    presupuesto_total = serializers.FloatField()
    proyectos_activos = serializers.IntegerField()
    empleados_por_departamento = serializers.ListField()
    proyectos_por_estado = serializers.ListField()
