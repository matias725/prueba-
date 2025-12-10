from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    info,
    DispositivoViewSet,
    MedicionViewSet,
    AlertaViewSet,
    ZonaViewSet,
    OrganizacionViewSet
)

# Configurar el router de Django REST Framework
router = DefaultRouter()
router.register(r'dispositivos', DispositivoViewSet, basename='dispositivo')
router.register(r'mediciones', MedicionViewSet, basename='medicion')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'zonas', ZonaViewSet, basename='zona')
router.register(r'organizaciones', OrganizacionViewSet, basename='organizacion')

urlpatterns = [
    path('info/', info, name='api-info'),
    path('', include(router.urls)),
]