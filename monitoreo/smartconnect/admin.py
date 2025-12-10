from django.contrib import admin
from .models import Departamento, Rol, UsuarioSmartConnect, Sensor, Barrera, Evento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']


@admin.register(UsuarioSmartConnect)
class UsuarioSmartConnectAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'departamento', 'activo']
    list_filter = ['rol', 'activo', 'departamento']
    search_fields = ['user__username']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['uid_mac', 'estado', 'usuario', 'departamento', 'activo']
    list_filter = ['estado', 'activo', 'departamento']
    search_fields = ['uid_mac', 'descripcion']


@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'departamento', 'activo']
    list_filter = ['estado', 'activo', 'departamento']
    search_fields = ['nombre']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'sensor', 'barrera', 'fecha_hora', 'resultado']
    list_filter = ['tipo', 'fecha_hora', 'departamento']
    search_fields = ['sensor__uid_mac', 'descripcion']
    ordering = ['-fecha_hora']
