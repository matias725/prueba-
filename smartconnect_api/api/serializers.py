from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sensor, Departamento, Evento, Barrera
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class DepartamentoSerializer(serializers.ModelSerializer):
    sensores_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ('id', 'nombre', 'descripcion', 'ubicacion', 'activo', 'creado_en', 'actualizado_en', 'sensores_count')
        read_only_fields = ('id', 'creado_en', 'actualizado_en')

    def get_sensores_count(self, obj):
        return obj.sensores.count()

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener mínimo 3 caracteres")
        return value


class SensorSerializer(serializers.ModelSerializer):
    usuario_asignado_username = serializers.CharField(source='usuario_asignado.username', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Sensor
        fields = (
            'id', 'uid', 'nombre', 'tipo', 'estado', 'usuario_asignado',
            'usuario_asignado_username', 'departamento', 'departamento_nombre',
            'creado_en', 'actualizado_en'
        )
        read_only_fields = ('id', 'creado_en', 'actualizado_en')

    def validate_uid(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El UID debe tener mínimo 3 caracteres")
        # Validar que no exista otro sensor con el mismo UID
        request = self.context.get('request')
        if request and request.method == 'POST':
            if Sensor.objects.filter(uid=value).exists():
                raise serializers.ValidationError("Este UID ya está registrado")
        return value

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener mínimo 3 caracteres")
        return value

    def validate_estado(self, value):
        valid_states = ['activo', 'inactivo', 'bloqueado', 'perdido']
        if value not in valid_states:
            raise serializers.ValidationError(f"Estado debe ser uno de: {', '.join(valid_states)}")
        return value


class BarreraSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Barrera
        fields = ('id', 'nombre', 'departamento', 'departamento_nombre', 'estado', 'modo_manual', 'creado_en', 'actualizado_en')
        read_only_fields = ('id', 'creado_en', 'actualizado_en')

    def validate_estado(self, value):
        if value not in ['abierta', 'cerrada']:
            raise serializers.ValidationError("Estado debe ser 'abierta' o 'cerrada'")
        return value


class EventoSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Evento
        fields = (
            'id', 'sensor', 'sensor_nombre', 'departamento', 'departamento_nombre',
            'tipo', 'resultado', 'descripcion', 'usuario', 'usuario_username',
            'creado_en'
        )
        read_only_fields = ('id', 'creado_en')

    def validate_tipo(self, value):
        valid_types = ['acceso_intento', 'acceso_permitido', 'acceso_denegado', 'barrera_abierta', 'barrera_cerrada']
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo debe ser uno de: {', '.join(valid_types)}")
        return value

    def validate_resultado(self, value):
        if value and value not in ['permitido', 'denegado']:
            raise serializers.ValidationError("Resultado debe ser 'permitido' o 'denegado'")
        return value
