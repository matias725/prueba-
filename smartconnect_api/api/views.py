from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Sensor, Departamento, Evento, Barrera
from .serializers import (
    UserSerializer, SensorSerializer, DepartamentoSerializer,
    EventoSerializer, BarreraSerializer
)
from .permissions import IsAdmin, IsOperador


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para Departamentos.
    
    Permisos:
    - Admin: CRUD completo
    - Operador: Solo lectura
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener solo departamentos activos"""
        departamentos = Departamento.objects.filter(activo=True)
        serializer = self.get_serializer(departamentos, many=True)
        return Response(serializer.data)


class SensorViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para Sensores RFID.
    
    Permisos:
    - Admin: CRUD completo
    - Operador: Solo lectura
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['estado', 'departamento', 'tipo']
    search_fields = ['uid', 'nombre']
    ordering_fields = ['creado_en', 'nombre']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'])
    def registrar_acceso(self, request):
        """
        Registra un intento de acceso con un sensor.
        
        Requerido: uid, departamento_id
        """
        uid = request.data.get('uid')
        departamento_id = request.data.get('departamento_id')

        if not uid or not departamento_id:
            return Response(
                {'error': 'uid y departamento_id son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sensor = Sensor.objects.get(uid=uid)
            departamento = Departamento.objects.get(id=departamento_id)

            # Validar estado del sensor
            if sensor.estado == 'bloqueado':
                Evento.objects.create(
                    sensor=sensor,
                    departamento=departamento,
                    tipo='acceso_intento',
                    resultado='denegado',
                    descripcion='Sensor bloqueado'
                )
                return Response(
                    {'error': 'Acceso denegado. Sensor bloqueado.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if sensor.estado == 'perdido':
                Evento.objects.create(
                    sensor=sensor,
                    departamento=departamento,
                    tipo='acceso_intento',
                    resultado='denegado',
                    descripcion='Sensor reportado como perdido'
                )
                return Response(
                    {'error': 'Acceso denegado. Sensor reportado como perdido.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if sensor.estado == 'inactivo':
                Evento.objects.create(
                    sensor=sensor,
                    departamento=departamento,
                    tipo='acceso_intento',
                    resultado='denegado',
                    descripcion='Sensor inactivo'
                )
                return Response(
                    {'error': 'Acceso denegado. Sensor inactivo.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Acceso permitido
            evento = Evento.objects.create(
                sensor=sensor,
                departamento=departamento,
                tipo='acceso_permitido',
                resultado='permitido',
                descripcion='Acceso permitido',
                usuario=sensor.usuario_asignado
            )

            # Abrir barrera automáticamente
            try:
                barrera = Barrera.objects.get(departamento=departamento)
                barrera.estado = 'abierta'
                barrera.save()
            except Barrera.DoesNotExist:
                pass

            return Response({
                'mensaje': 'Acceso permitido',
                'sensor': SensorSerializer(sensor).data,
                'evento_id': evento.id
            }, status=status.HTTP_200_OK)

        except Sensor.DoesNotExist:
            return Response(
                {'error': 'Sensor no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Departamento.DoesNotExist:
            return Response(
                {'error': 'Departamento no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def bloquear(self, request, pk=None):
        """Bloquear un sensor"""
        if not request.user.is_staff:
            return Response(
                {'error': 'No tiene permisos para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        sensor = self.get_object()
        sensor.estado = 'bloqueado'
        sensor.save()
        return Response({'mensaje': 'Sensor bloqueado'})

    @action(detail=True, methods=['post'])
    def marcar_perdido(self, request, pk=None):
        """Marcar un sensor como perdido"""
        if not request.user.is_staff:
            return Response(
                {'error': 'No tiene permisos para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        sensor = self.get_object()
        sensor.estado = 'perdido'
        sensor.save()
        return Response({'mensaje': 'Sensor marcado como perdido'})


class BarreraViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para control de Barreras.
    """
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def abrir(self, request, pk=None):
        """Abrir barrera manualmente"""
        if not request.user.is_staff:
            return Response(
                {'error': 'No tiene permisos para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        barrera = self.get_object()
        barrera.estado = 'abierta'
        barrera.modo_manual = True
        barrera.save()

        # Registrar evento
        Evento.objects.create(
            sensor_id=1,  # Ajustar según necesidad
            departamento=barrera.departamento,
            tipo='barrera_abierta',
            resultado='permitido',
            descripcion='Barrera abierta manualmente',
            usuario=request.user
        )

        return Response({'mensaje': 'Barrera abierta', 'estado': barrera.estado})

    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cerrar barrera manualmente"""
        if not request.user.is_staff:
            return Response(
                {'error': 'No tiene permisos para esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        barrera = self.get_object()
        barrera.estado = 'cerrada'
        barrera.modo_manual = True
        barrera.save()

        # Registrar evento
        Evento.objects.create(
            sensor_id=1,  # Ajustar según necesidad
            departamento=barrera.departamento,
            tipo='barrera_cerrada',
            resultado='permitido',
            descripcion='Barrera cerrada manualmente',
            usuario=request.user
        )

        return Response({'mensaje': 'Barrera cerrada', 'estado': barrera.estado})


class EventoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet para Eventos (solo lectura).
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['sensor', 'departamento', 'tipo', 'resultado']
    ordering_fields = ['creado_en']
    ordering = ['-creado_en']

    @action(detail=False, methods=['get'])
    def ultimos(self, request):
        """Obtener últimos 10 eventos"""
        eventos = Evento.objects.all()[:10]
        serializer = self.get_serializer(eventos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_sensor(self, request):
        """Obtener eventos por sensor"""
        sensor_id = request.query_params.get('sensor_id')
        if not sensor_id:
            return Response(
                {'error': 'sensor_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        eventos = Evento.objects.filter(sensor_id=sensor_id)
        serializer = self.get_serializer(eventos, many=True)
        return Response(serializer.data)
