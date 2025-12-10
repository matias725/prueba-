from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartamentoViewSet,
    EmpleadoViewSet,
    ProyectoViewSet,
    RegistroTiempoViewSet,
    DashboardViewSet
)

# Configurar el router de DRF
router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'empleados', EmpleadoViewSet, basename='empleado')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'registros-tiempo', RegistroTiempoViewSet, basename='registrostiempo')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

app_name = 'rrhh'

urlpatterns = [
    path('', include(router.urls)),
]
