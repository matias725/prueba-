from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    DepartamentoViewSet, SensorViewSet, BarreraViewSet, EventoViewSet
)

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'barreras', BarreraViewSet, basename='barrera')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router
    path('', include(router.urls)),
]
