from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Departamento, Rol, UsuarioSmartConnect, Sensor, Barrera, Evento
from .serializers import (DepartamentoSerializer, RolSerializer, UserSerializer, 
                          UsuarioSmartConnectSerializer, SensorSerializer, 
                          BarreraSerializer, EventoSerializer)


class IsAdmin(permissions.BasePermission):
    """Permiso personalizado para admin."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Permitir superusuarios o staff sin depender del perfil
        if user.is_superuser or user.is_staff:
            return True
        profile = getattr(user, 'smartconnect_profile', None)
        if not profile or not profile.rol:
            return False
        return profile.rol.nombre == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin puede modificar, operador solo lectura."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Lectura permitida a cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_superuser or user.is_staff:
            return True
        profile = getattr(user, 'smartconnect_profile', None)
        if not profile or not profile.rol:
            return False
        return profile.rol.nombre == 'admin'


class InfoAPIView(APIView):
    """Endpoint /api/info/ con información del proyecto."""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        info = {
            "autor": ["Matías Ahumada"],
            "asignatura": "Programación Back End",
            "proyecto": "SmartConnect - Sistema de Control de Acceso RFID",
            "descripcion": "API RESTful para gestión de sensores RFID, control de acceso, departamentos y eventos en sistema inteligente de control de acceso",
            "version": "1.0"
        }
        return Response(info, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Endpoint para login y obtención de JWT."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {"error": "Username y password requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = get_object_or_404(User, username=username)
        
        if not user.check_password(password):
            return Response(
                {"error": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {"error": "Usuario inactivo"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            profile = user.smartconnect_profile
            if not profile.activo:
                return Response(
                    {"error": "Perfil inactivo"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except UsuarioSmartConnect.DoesNotExist:
            return Response(
                {"error": "Usuario sin perfil SmartConnect"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rol': profile.rol.nombre if profile.rol else None
            }
        }, status=status.HTTP_200_OK)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """CRUD de Departamentos - Solo admin puede modificar."""
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['activo']


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    """Ver roles del sistema (solo lectura)."""
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioSmartConnectViewSet(viewsets.ModelViewSet):
    """CRUD de Usuarios - Solo admin."""
    queryset = UsuarioSmartConnect.objects.all()
    serializer_class = UsuarioSmartConnectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class SensorViewSet(viewsets.ModelViewSet):
    """CRUD de Sensores - Admin modifica, operador lectura."""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['estado', 'activo', 'departamento']
    search_fields = ['uid_mac', 'descripcion']
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def registrar_sensor(self, request):
        """Endpoint para registrar un nuevo sensor."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BarreraViewSet(viewsets.ModelViewSet):
    """CRUD de Barreras - Admin modifica, operador lectura."""
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['estado', 'activo', 'departamento']
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def cambiar_estado(self, request, pk=None):
        """Cambia el estado de la barrera (abrir/cerrar)."""
        barrera = self.get_object()
        nuevo_estado = request.data.get('estado') or request.data.get('nuevo_estado')
        
        if nuevo_estado not in ['abierta', 'cerrada']:
            return Response(
                {"error": "Estado inválido. Debe ser 'abierta' o 'cerrada'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        barrera.estado = nuevo_estado
        barrera.save()
        
        return Response(
            {"mensaje": f"Barrera {barrera.nombre} está ahora {nuevo_estado}"},
            status=status.HTTP_200_OK
        )


class EventoViewSet(viewsets.ModelViewSet):
    """CRUD de Eventos - Admin modifica, operador solo lectura."""
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['tipo', 'departamento', 'sensor']
    ordering_fields = ['fecha_hora']
    ordering = ['-fecha_hora']
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def registrar_acceso(self, request):
        """Registra un evento de acceso por sensor RFID."""
        uid_mac = request.data.get('uid_mac')
        barrera_id = request.data.get('barrera_id')
        
        if not uid_mac:
            return Response(
                {"error": "UID/MAC del sensor requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            sensor = Sensor.objects.get(uid_mac=uid_mac)
        except Sensor.DoesNotExist:
            return Response(
                {"error": f"Sensor con UID {uid_mac} no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validar sensor
        if sensor.estado != 'activo':
            evento = Evento.objects.create(
                tipo='acceso_denegado',
                sensor=sensor,
                resultado=f"Sensor en estado {sensor.estado}"
            )
            return Response(
                {
                    "tipo": "acceso_denegado",
                    "mensaje": f"Acceso denegado. Sensor en estado: {sensor.estado}",
                    "evento_id": evento.id
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Acceso permitido
        evento = Evento.objects.create(
            tipo='acceso_permitido',
            sensor=sensor,
            departamento=sensor.departamento,
            usuario=sensor.usuario,
            resultado='permitido'
        )
        
        # Abrir barrera si existe
        if barrera_id:
            try:
                barrera = Barrera.objects.get(id=barrera_id)
                barrera.estado = 'abierta'
                barrera.save()
                evento.barrera = barrera
                evento.save()
            except Barrera.DoesNotExist:
                pass
        
        return Response(
            {
                "tipo": "acceso_permitido",
                "mensaje": "Acceso permitido",
                "sensor": sensor.uid_mac,
                "evento_id": evento.id
            },
            status=status.HTTP_200_OK
        )
