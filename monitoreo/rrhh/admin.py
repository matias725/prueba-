from django.contrib import admin
from .models import Departamento, Empleado, Proyecto, RegistroTiempo


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'gerente', 'presupuesto', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'user', 'puesto', 'departamento', 'salario', 'estado', 'fecha_contratacion')
    list_filter = ('estado', 'departamento', 'fecha_contratacion')
    search_fields = ('numero_empleado', 'user__first_name', 'user__last_name', 'email')
    readonly_fields = ('fecha_creacion', 'actualizado', 'antiguedad_meses', 'dias_trabajados')
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('user',)
        }),
        ('Información de Empleado', {
            'fields': ('numero_empleado', 'puesto', 'departamento', 'salario', 'estado')
        }),
        ('Contacto', {
            'fields': ('telefono', 'direccion')
        }),
        ('Fechas', {
            'fields': ('fecha_contratacion', 'fecha_creacion', 'actualizado', 'antiguedad_meses', 'dias_trabajados')
        })
    )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'gerente_proyecto', 'estado', 'porcentaje_completado', 'fecha_inicio', 'fecha_fin_estimada')
    list_filter = ('estado', 'departamento', 'fecha_inicio')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'actualizado', 'dias_para_vencer', 'total_horas_registradas')
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('nombre', 'descripcion', 'estado')
        }),
        ('Asignación', {
            'fields': ('departamento', 'gerente_proyecto')
        }),
        ('Presupuesto y Progreso', {
            'fields': ('presupuesto', 'porcentaje_completado', 'total_horas_registradas')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real', 'dias_para_vencer')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'actualizado'),
            'classes': ('collapse',)
        })
    )


@admin.register(RegistroTiempo)
class RegistroTiempoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'proyecto', 'fecha', 'horas', 'validado', 'fecha_creacion')
    list_filter = ('validado', 'fecha', 'proyecto')
    search_fields = ('empleado__user__first_name', 'empleado__user__last_name', 'proyecto__nombre')
    readonly_fields = ('fecha_creacion', 'costo_hora')
    fieldsets = (
        ('Asignación', {
            'fields': ('empleado', 'proyecto')
        }),
        ('Tiempo', {
            'fields': ('fecha', 'horas', 'costo_hora')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Validación', {
            'fields': ('validado', 'fecha_creacion')
        })
    )
    actions = ['marcar_validado', 'marcar_no_validado']

    def marcar_validado(self, request, queryset):
        count = queryset.update(validado=True)
        self.message_user(request, f'{count} registros marcados como validados.')
    marcar_validado.short_description = "Marcar seleccionados como validados"

    def marcar_no_validado(self, request, queryset):
        count = queryset.update(validado=False)
        self.message_user(request, f'{count} registros marcados como no validados.')
    marcar_no_validado.short_description = "Marcar seleccionados como no validados"
