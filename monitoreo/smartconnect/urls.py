from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (InfoAPIView, LoginAPIView, DepartamentoViewSet, RolViewSet,
                    UsuarioSmartConnectViewSet, SensorViewSet, BarreraViewSet, EventoViewSet)

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'usuarios', UsuarioSmartConnectViewSet, basename='usuario')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'barreras', BarreraViewSet, basename='barrera')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    path('info/', InfoAPIView.as_view(), name='info'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('', include(router.urls)),
]
