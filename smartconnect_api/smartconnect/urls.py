"""
URL configuration for smartconnect project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Endpoint informativo de la API"""
    return Response({
        "autor": ["Matías [Apellido Paterno] [Apellido Materno]"],  # CAMBIA ESTO POR TU NOMBRE COMPLETO
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect - Sistema de Control de Acceso Inteligente",
        "descripcion": "API RESTful para gestionar sensores RFID, usuarios, departamentos, eventos de acceso y control de barreras. Implementa autenticación JWT, roles de usuario y trazabilidad completa.",
        "version": "1.0"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def handler404(request, exception=None):
    """Handler personalizado para errores 404"""
    return Response({
        "error": "Recurso no encontrado",
        "mensaje": "La ruta solicitada no existe en esta API",
        "status_code": 404,
        "ruta_solicitada": request.path
    }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def handler500(request):
    """Handler personalizado para errores 500"""
    return Response({
        "error": "Error interno del servidor",
        "mensaje": "Ha ocurrido un error inesperado. Por favor contacte al administrador.",
        "status_code": 500
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/info/', api_info, name='api-info'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
]

# Handlers de errores personalizados
handler404 = 'smartconnect.urls.handler404'
handler500 = 'smartconnect.urls.handler500'
