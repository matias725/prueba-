from django.contrib import admin
from .models import Departamento, Sensor, Evento, Barrera

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'activo', 'creado_en')
    search_fields = ('nombre',)
    list_filter = ('activo', 'creado_en')


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'uid', 'tipo', 'estado', 'departamento', 'usuario_asignado', 'creado_en')
    search_fields = ('nombre', 'uid')
    list_filter = ('estado', 'tipo', 'departamento', 'creado_en')
    readonly_fields = ('creado_en', 'actualizado_en')


@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'estado', 'modo_manual')
    search_fields = ('nombre',)
    list_filter = ('estado', 'modo_manual')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'sensor', 'departamento', 'resultado', 'usuario', 'creado_en')
    search_fields = ('tipo', 'sensor__nombre')
    list_filter = ('tipo', 'resultado', 'creado_en', 'departamento')
    readonly_fields = ('creado_en',)
