from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Departamento, Rol, UsuarioSmartConnect, Sensor, Barrera, Evento


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'ubicacion', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UsuarioSmartConnectSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = UsuarioSmartConnect
        fields = ['id', 'user', 'rol', 'rol_nombre', 'departamento', 'departamento_nombre', 'activo', 'fecha_creacion']
        read_only_fields = ['id', 'user', 'fecha_creacion']


class SensorSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'uid_mac', 'descripcion', 'estado', 'usuario', 'usuario_nombre', 
                  'departamento', 'departamento_nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_uid_mac(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El UID/MAC debe tener al menos 3 caracteres.")
        return value


class BarreraSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Barrera
        fields = ['id', 'nombre', 'descripcion', 'estado', 'departamento', 
                  'departamento_nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class EventoSerializer(serializers.ModelSerializer):
    sensor_uid = serializers.CharField(source='sensor.uid_mac', read_only=True)
    barrera_nombre = serializers.CharField(source='barrera.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Evento
        fields = ['id', 'tipo', 'sensor', 'sensor_uid', 'barrera', 'barrera_nombre', 
                  'departamento', 'usuario', 'usuario_nombre', 'descripcion', 'fecha_hora', 'resultado']
        read_only_fields = ['id', 'fecha_hora']
