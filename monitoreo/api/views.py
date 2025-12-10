from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dispositivos.models import Dispositivo, Medicion, Alerta, Zona
from usuarios.models import Organizacion
from .serializers import (
    DispositivoSerializer, DispositivoDetalleSerializer,
    MedicionSerializer, AlertaSerializer, ZonaSerializer,
    OrganizacionSerializer
)


def info(request):
    datos = {
        "proyecto": "EcoEnergy",
        "version": "1.0",
        "autor": "matias"
    }
    return JsonResponse(datos)


class ZonaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar zonas
    Permite listar, crear, actualizar y eliminar zonas
    """
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'organizacion__nombre']
    ordering_fields = ['nombre', 'id']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = Zona.objects.select_related('organizacion')
        organizacion_id = self.request.query_params.get('organizacion', None)
        if organizacion_id:
            queryset = queryset.filter(organizacion_id=organizacion_id)
        return queryset

    @action(detail=True, methods=['get'])
    def dispositivos(self, request, pk=None):
        """Obtiene todos los dispositivos de una zona"""
        zona = self.get_object()
        dispositivos = zona.dispositivo_set.all()
        serializer = DispositivoSerializer(dispositivos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtiene estadísticas de consumo de una zona"""
        zona = self.get_object()
        dispositivos = zona.dispositivo_set.all()
        
        total_dispositivos = dispositivos.count()
        consumo_total = Medicion.objects.filter(
            dispositivo__zona=zona
        ).aggregate(total=Sum('consumo'))['total'] or 0
        
        alertas_graves = Alerta.objects.filter(
            dispositivo__zona=zona,
            gravedad='Grave'
        ).count()
        
        return Response({
            'zona': zona.nombre,
            'total_dispositivos': total_dispositivos,
            'consumo_total_kwh': round(consumo_total, 2),
            'alertas_graves': alertas_graves,
            'watts_promedio': round(dispositivos.aggregate(Avg('watts'))['watts__avg'] or 0, 2)
        })


class DispositivoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar dispositivos
    Soporta operaciones CRUD completas y filtros avanzados
    """
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'categoria', 'zona__nombre']
    ordering_fields = ['nombre', 'categoria', 'watts', 'id']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = Dispositivo.objects.select_related('zona', 'zona__organizacion')
        
        # Filtros opcionales
        categoria = self.request.query_params.get('categoria', None)
        zona_id = self.request.query_params.get('zona', None)
        watts_min = self.request.query_params.get('watts_min', None)
        watts_max = self.request.query_params.get('watts_max', None)
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if zona_id:
            queryset = queryset.filter(zona_id=zona_id)
        if watts_min:
            queryset = queryset.filter(watts__gte=watts_min)
        if watts_max:
            queryset = queryset.filter(watts__lte=watts_max)
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DispositivoDetalleSerializer
        return DispositivoSerializer

    @action(detail=True, methods=['get'])
    def mediciones(self, request, pk=None):
        """Obtiene todas las mediciones de un dispositivo"""
        dispositivo = self.get_object()
        mediciones = dispositivo.medicion_set.all()
        
        # Paginación opcional
        limit = request.query_params.get('limit', None)
        if limit:
            mediciones = mediciones[:int(limit)]
            
        serializer = MedicionSerializer(mediciones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def alertas(self, request, pk=None):
        """Obtiene todas las alertas de un dispositivo"""
        dispositivo = self.get_object()
        alertas = dispositivo.alerta_set.all()
        
        # Filtro por gravedad
        gravedad = request.query_params.get('gravedad', None)
        if gravedad:
            alertas = alertas.filter(gravedad=gravedad)
            
        serializer = AlertaSerializer(alertas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def consumo_total(self, request, pk=None):
        """Calcula el consumo total de un dispositivo"""
        dispositivo = self.get_object()
        total = dispositivo.medicion_set.aggregate(total=Sum('consumo'))['total'] or 0
        promedio = dispositivo.medicion_set.aggregate(promedio=Avg('consumo'))['promedio'] or 0
        cantidad = dispositivo.medicion_set.count()
        
        return Response({
            'dispositivo': dispositivo.nombre,
            'consumo_total_kwh': round(total, 2),
            'consumo_promedio_kwh': round(promedio, 2),
            'total_mediciones': cantidad,
            'watts_nominales': dispositivo.watts
        })

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Agrupa dispositivos por categoría con estadísticas"""
        categorias = Dispositivo.objects.values('categoria').annotate(
            total=Count('id'),
            watts_total=Sum('watts'),
            watts_promedio=Avg('watts')
        ).order_by('categoria')
        
        return Response(list(categorias))


class MedicionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar mediciones de consumo
    """
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha', 'consumo']
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = Medicion.objects.select_related('dispositivo', 'dispositivo__zona')
        
        # Filtros
        dispositivo_id = self.request.query_params.get('dispositivo', None)
        zona_id = self.request.query_params.get('zona', None)
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        
        if dispositivo_id:
            queryset = queryset.filter(dispositivo_id=dispositivo_id)
        if zona_id:
            queryset = queryset.filter(dispositivo__zona_id=zona_id)
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
            
        return queryset

    @action(detail=False, methods=['get'])
    def estadisticas_generales(self, request):
        """Estadísticas generales de todas las mediciones"""
        stats = Medicion.objects.aggregate(
            total_mediciones=Count('id'),
            consumo_total=Sum('consumo'),
            consumo_promedio=Avg('consumo'),
            consumo_maximo=Sum('consumo')
        )
        
        return Response({
            'total_mediciones': stats['total_mediciones'] or 0,
            'consumo_total_kwh': round(stats['consumo_total'] or 0, 2),
            'consumo_promedio_kwh': round(stats['consumo_promedio'] or 0, 2),
            'consumo_maximo_kwh': round(stats['consumo_maximo'] or 0, 2)
        })


class AlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar alertas del sistema
    """
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['mensaje', 'dispositivo__nombre', 'gravedad']
    ordering_fields = ['fecha', 'gravedad']
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = Alerta.objects.select_related('dispositivo', 'dispositivo__zona')
        
        # Filtros
        dispositivo_id = self.request.query_params.get('dispositivo', None)
        gravedad = self.request.query_params.get('gravedad', None)
        zona_id = self.request.query_params.get('zona', None)
        
        if dispositivo_id:
            queryset = queryset.filter(dispositivo_id=dispositivo_id)
        if gravedad:
            queryset = queryset.filter(gravedad=gravedad)
        if zona_id:
            queryset = queryset.filter(dispositivo__zona_id=zona_id)
            
        return queryset

    @action(detail=False, methods=['get'])
    def por_gravedad(self, request):
        """Agrupa alertas por nivel de gravedad"""
        alertas = Alerta.objects.values('gravedad').annotate(
            total=Count('id')
        ).order_by('-total')
        
        return Response(list(alertas))

    @action(detail=False, methods=['get'])
    def criticas(self, request):
        """Obtiene solo las alertas graves"""
        alertas = Alerta.objects.filter(gravedad='Grave')
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)


class OrganizacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para organizaciones
    """
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

    @action(detail=True, methods=['get'])
    def zonas(self, request, pk=None):
        """Obtiene todas las zonas de una organización"""
        organizacion = self.get_object()
        zonas = organizacion.zona_set.all()
        serializer = ZonaSerializer(zonas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def resumen(self, request, pk=None):
        """Resumen completo de una organización"""
        organizacion = self.get_object()
        zonas = organizacion.zona_set.all()
        
        total_zonas = zonas.count()
        total_dispositivos = Dispositivo.objects.filter(zona__organizacion=organizacion).count()
        consumo_total = Medicion.objects.filter(
            dispositivo__zona__organizacion=organizacion
        ).aggregate(total=Sum('consumo'))['total'] or 0
        
        alertas_graves = Alerta.objects.filter(
            dispositivo__zona__organizacion=organizacion,
            gravedad='Grave'
        ).count()
        
        return Response({
            'organizacion': organizacion.nombre,
            'total_zonas': total_zonas,
            'total_dispositivos': total_dispositivos,
            'consumo_total_kwh': round(consumo_total, 2),
            'alertas_graves': alertas_graves
        })
