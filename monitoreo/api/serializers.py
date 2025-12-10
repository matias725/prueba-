from rest_framework import serializers
from dispositivos.models import Dispositivo, Medicion, Alerta, Zona
from usuarios.models import Organizacion


class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = ['id', 'nombre']


class ZonaSerializer(serializers.ModelSerializer):
    organizacion_nombre = serializers.CharField(source='organizacion.nombre', read_only=True)
    
    class Meta:
        model = Zona
        fields = ['id', 'nombre', 'organizacion', 'organizacion_nombre']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value


class DispositivoSerializer(serializers.ModelSerializer):
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)
    organizacion_nombre = serializers.CharField(source='zona.organizacion.nombre', read_only=True)
    
    class Meta:
        model = Dispositivo
        fields = ['id', 'nombre', 'categoria', 'zona', 'zona_nombre', 'organizacion_nombre', 'watts']
        read_only_fields = ['id']

    def validate_watts(self, value):
        if value < 0:
            raise serializers.ValidationError("El consumo en watts no puede ser negativo")
        if value > 100000:
            raise serializers.ValidationError("El consumo en watts parece demasiado alto")
        return value

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        return value


class MedicionSerializer(serializers.ModelSerializer):
    dispositivo_nombre = serializers.CharField(source='dispositivo.nombre', read_only=True)
    categoria = serializers.CharField(source='dispositivo.categoria', read_only=True)
    
    class Meta:
        model = Medicion
        fields = ['id', 'dispositivo', 'dispositivo_nombre', 'categoria', 'fecha', 'consumo']
        read_only_fields = ['id', 'fecha']

    def validate_consumo(self, value):
        if value < 0:
            raise serializers.ValidationError("El consumo no puede ser negativo")
        if value > 10000:
            raise serializers.ValidationError("El consumo parece demasiado alto")
        return value


class AlertaSerializer(serializers.ModelSerializer):
    dispositivo_nombre = serializers.CharField(source='dispositivo.nombre', read_only=True)
    zona_nombre = serializers.CharField(source='dispositivo.zona.nombre', read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'dispositivo', 'dispositivo_nombre', 'zona_nombre', 'fecha', 'mensaje', 'gravedad']
        read_only_fields = ['id', 'fecha']

    def validate_mensaje(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres")
        return value


class DispositivoDetalleSerializer(serializers.ModelSerializer):
    """Serializer con información detallada del dispositivo incluyendo mediciones y alertas recientes"""
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)
    organizacion_nombre = serializers.CharField(source='zona.organizacion.nombre', read_only=True)
    mediciones_recientes = serializers.SerializerMethodField()
    alertas_recientes = serializers.SerializerMethodField()
    consumo_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Dispositivo
        fields = ['id', 'nombre', 'categoria', 'zona', 'zona_nombre', 'organizacion_nombre', 
                  'watts', 'mediciones_recientes', 'alertas_recientes', 'consumo_total']

    def get_mediciones_recientes(self, obj):
        mediciones = obj.medicion_set.all()[:5]
        return MedicionSerializer(mediciones, many=True).data

    def get_alertas_recientes(self, obj):
        alertas = obj.alerta_set.all()[:5]
        return AlertaSerializer(alertas, many=True).data

    def get_consumo_total(self, obj):
        total = sum(m.consumo for m in obj.medicion_set.all())
        return round(total, 2)
